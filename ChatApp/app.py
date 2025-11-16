from google import genai
from flask import (
    Flask,
    request,
    redirect,
    render_template,
    session,
    flash,
    abort,
    url_for,
    jsonify,
)
from datetime import timedelta
import hashlib
import uuid
import re
import os
import json

from pydantic import BaseModel, Field
from typing import List, Optional

from models import User, Group, Message, Member, eatReaction
from util.assets import bundle_css_files


# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

# ブラウザに静的ファイル（CSSや画像など）を長くキャッシュさせる設定。
# 開発中は変更がすぐ反映されないことがあるため、コメントアウトするのが無難です。
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 2678400

# 複数のCSSファイルを1つにまとめて圧縮（バンドル）する処理を実行。
bundle_css_files(app)


# ルートページ処理
@app.route("/", methods=["GET"])
def index_process():
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    return redirect(url_for("home_view"))


# ログイン処理
@app.route("/login", methods=["POST"])
def login_process():
    email = request.form.get("email")
    password = request.form.get("password")
    if email == "" or password == "":
        flash("この項目は必須入力です")
    else:
        user = User.find_by_email(email)
        if user is None:
            flash("このユーザーは存在しません")
        else:
            hashPassword = hashlib.sha256(password.encode("utf-8")).hexdigest()

            if hashPassword != user["password"]:
                flash("パスワードが違います")
            else:
                session["uid"] = user["id"]
                return redirect(url_for("home_view"))
    return redirect(url_for("login_view"))


# ログイン画面表示
@app.route("/login", methods=["GET"])
def login_view():
    uid = session.get("uid")
    if uid is None:
        return render_template("auth/login.html")

    return redirect(
        url_for("home_view")
    )  # ログイン済みの場合、グループ一覧にリダイレクト


# ユーザー新規登録画面表示
@app.route("/signup", methods=["GET"])
def signup_view():
    return render_template("auth/signup.html")


# ユーザー新規登録処理
@app.route("/signup", methods=["POST"])
def signup_process():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    passwordConfirmation = request.form.get("passwordConfirmation")

    if name == "" or email == "" or password == "" or passwordConfirmation == "":
        flash("空のフォームがあります")
    elif password != passwordConfirmation:
        flash("二つのパスワードが一致しません")
    elif re.match(EMAIL_PATTERN, email) is None:
        flash("メールアドレスが正しくありません")
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        registered_user = User.find_by_email(email)
        if registered_user != None:
            flash("メールアドレスがすでに登録されています")
        else:
            User.create(uid, name, email, password)
            UserID = str(uid)
            session["uid"] = UserID
            return redirect(url_for("home_view"))
    return redirect(url_for("signup_view"))


# ログアウト処理
@app.route("/logout")
def logout_process():
    session.clear()
    return redirect(url_for("login_view"))


# グループ一覧画面表示
@app.route("/home", methods=["GET"])
def home_view():
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    else:
        groups = Group.find_by_uid(uid)
        # groups.reverse()
        return render_template("groups.html", groups=groups, uid=uid)


# グループリダイレクト処理
@app.route("/group", methods=["GET"])
def group_process():
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    else:
        return redirect(url_for("home_view"))


# グループ作成処理
@app.route("/group", methods=["POST"])
def create_group():
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    else:
        group_name = request.form.get("groupName")

        if group_name == "":
            return redirect(url_for("home_view"))
        else:
            gid = Group.create(uid, group_name)

            Member.add(uid, gid)  # user_groupsテーブルに作成者を登録
            return redirect(url_for("message_view", gid=gid))


# グループ名編集処理
@app.route("/group/<gid>/update", methods=["POST"])
def update_group(gid):
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    else:
        group = Group.find_by_gid(gid)
        if group is None:
            flash("グループが存在しません")
        elif uid != group["created_by"]:
            flash("グループ名はグループ作成者のみ編集可能です")
        else:
            new_group_name = request.form.get("newGroupName")
            Group.update(gid, new_group_name)
            return redirect(url_for("message_view", gid=gid))


# グループ削除処理
@app.route("/group/<gid>/delete", methods=["POST"])
def delete_group(gid):
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    else:
        group = Group.find_by_gid(gid)
        if group is None:
            flash("グループが存在しません")
        elif uid != group["created_by"]:
            flash("グループはグループ作成者のみ削除可能です")
        else:
            Group.delete(gid)

        return redirect(url_for("home_view"))


# ユーザー招待処理
@app.route("/group/<gid>/member/add", methods=["POST"])
def add_member(gid):
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    email = request.form.get("email")
    reopen_modal = None
    if email == "":
        flash("空のフォームがあります")
        reopen_modal = "add-member"
    else:
        group = Group.find_by_gid(gid)
        if group is None:
            flash("グループが存在しません")
        elif uid != group["created_by"]:
            flash("ユーザーの招待はグループ作成者のみ削除可能です")
        else:
            registerd_user = User.find_by_email(email)
            if registerd_user is None:
                flash("このユーザーは存在しません")
                reopen_modal = "add-member"
            else:
                members = Member.get_all(gid)
                new_member_uid = registerd_user["id"]
                is_member = (
                    True
                    if new_member_uid in [member.get("id") for member in members]
                    else False
                )
                if is_member:
                    flash("すでにこのグループに参加しているユーザーです")
                    reopen_modal = "add-member"
                else:
                    Member.add(new_member_uid, gid)
        return redirect(url_for("message_view", gid=gid, reopen_modal=reopen_modal))


# メッセージ一覧画面表示（各グループ内で、そのグループに属している全メッセージを表示させる）
@app.route("/group/<gid>", methods=["GET"])
def message_view(gid):
    reopen_modal = request.args.get("reopen_modal")
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    else:
        group = Group.find_by_gid(gid)
        if group is None:
            flash("グループが存在しません")
            return redirect(url_for("home_view"))

        members = Member.get_all(gid)
        is_member = True if uid in [member.get("id") for member in members] else False
        if not is_member:
            flash("参加していないグループです")
            return redirect(url_for("home_view"))
        else:
            messages = Message.get_all(gid)
            return render_template(
                "messages.html",
                messages=messages,
                group=group,
                members=members,
                uid=uid,
                reopen_modal=reopen_modal,
            )


# メッセージ作成処理
@app.route("/group/<gid>/message", methods=["POST"])
def create_message(gid):
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    else:
        group = Group.find_by_gid(gid)
        if group is None:
            flash("グループが存在しません")
            return redirect(url_for("home_view"))

        members = Member.get_all(gid)
        is_member = True if uid in [member.get("id") for member in members] else False
        if not is_member:
            flash("参加していないグループです")
            return redirect(url_for("home_view"))
        else:
            message = request.form.get("message")
            if message:
                Message.create(uid, gid, message)
                return redirect(url_for("message_view", gid=gid))


# メッセージ削除処理
@app.route("/group/<gid>/message/delete", methods=["POST"])
def delete_message(gid):
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    else:
        group = Group.find_by_gid(gid)
        if group is None:
            flash("グループが存在しません")
            return redirect(url_for("home_view"))
        members = Member.get_all(gid)
        is_member = True if uid in [member.get("id") for member in members] else False
        if not is_member:
            flash("参加していないグループです")
            return redirect(url_for("home_view"))
        else:
            message_id = request.form.get("message_id")
            message = Message.find_by_mid(message_id)
            isMessageExist = True if not message else False
            if not isMessageExist:
                flash("メッセージが存在しません")
            elif message != None:
                if uid != message["uid"]:
                    flash("メッセージの作成者ではないため削除できません")
            else:
                Message.delete(message_id)
        return redirect(url_for("message_view", gid=gid))


# リアクション送信処理
@app.route("/group/<gid>/message/reaction", methods=["POST"])
def add_reaction(gid):
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    else:
        group = Group.find_by_gid(gid)
        if group is None:
            flash("グループが存在しません")
            return redirect(url_for("home_view"))

        members = Member.get_all(gid)
        is_member = True if uid in [member.get("id") for member in members] else False
        if not is_member:
            flash("参加していないグループです")
            return redirect(url_for("home_view"))
        else:
            message_id = request.form.get("message_id")
            message_creation_type = request.form.get("message_creation_type")

            if message_creation_type == "user":
                message = Message.find_by_mid(message_id)
                print(message)
                isMessageExist = True if message else False
                print(isMessageExist)
                if not isMessageExist:
                    flash("メッセージが存在しません")
                    return redirect(url_for("message_view", gid=gid))

            eatReaction.add(
                message_id,
                message_creation_type,
            )
        return redirect(url_for("message_view", gid=gid))


# AIメニュー候補リクエスト処理
@app.route("/group/<gid>/menu", methods=["POST"])
def ai_menu_process(gid):
    uid = session.get("uid")

    if uid is None:
        return (
            jsonify(
                {
                    "message": "ログインしていません",
                    "redirect_url": "/login",
                }
            ),
            200,
        )
    else:
        group = Group.find_by_gid(gid)

        if group is None:
            flash("グループが存在しません")
            return (
                jsonify(
                    {
                        "message": "グループが存在しません",
                        "redirect_url": "/login",
                    }
                ),
                200,
            )

        members = Member.get_all(gid)
        is_member = True if uid in [member.get("id") for member in members] else False
        if not is_member:
            flash("参加していないグループです")
            return (
                jsonify(
                    {
                        "message": "参加していないグループです",
                        "redirect_url": "/home",
                    }
                ),
                200,
            )
        else:
            request_data = request.get_json()
            print(request_data)

            # ---- Gemini APIの設定 ----
            class Ingredient(BaseModel):
                name: str = Field(description="Name of the ingredient.")
                quantity: str = Field(description="Quantity of the ingredient")
                unit: str = Field(description="Unit of the quantity")

            class Menu(BaseModel):
                menuId: str = Field(description="The id of the menu. start from 1")
                menuName: str = Field(description="The name of the recipe.")
                ingredients: List[Ingredient]
                instructions: List[str]

            class Menus(BaseModel):
                menus: list[Menu]

            try:
                client = genai.Client()
            except Exception as e:
                print(f"Gemini APIの初期化中にエラーが発生しました: {e}")
                abort(500)

            # ---- Gemini APIでメニュー作成を依頼 ---
            # プロンプト
            prompt = f"""
            あなたは献立のメニューアドバイザーです。JSON形式で送信されるデータに基づいて、献立を考えてください。
            このデータには
                - 今ある食材名（name）、分量（quantity)、分量の単位（unit)
                - 任意の希望リクエスト
                - 希望するメニュー数

            が記載されています。データは{request_data}です。

            # 最重要ルール
            - 回答は日本語にしてください。
            - 今ある食材は必ず使ってください。ただし、必ず今ある食材だけでできるメニューである必要はなく、追加の食材が必要になっても問題ありません。
            - 作り方の文章には必ず 1. ような番号をつけてください。この番号は1から始めてください。
            """

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": Menus.model_json_schema(),
                    },
                )
                ai_response = Menus.model_validate_json(response.text)
                print(ai_response)

                for index, menu in enumerate(ai_response.menus):
                    ai_message = []
                    menu_name = menu.menuName
                    ai_message.extend(
                        [f"メニュー{index + 1}: {menu_name}", "", "<材料>"]
                    )

                    for ingredient in menu.ingredients:
                        name = ingredient.name
                        quantity = ingredient.quantity
                        unit = ingredient.unit
                        ai_message.append(f"{name} {quantity}{unit}")

                    ai_message.extend(["", "<作り方> "])

                    for instruction in menu.instructions:
                        ai_message.append(instruction)

                    ai_message_string = "\n".join(ai_message)
                    print(ai_message_string)
                    Message.ai_create(gid, ai_message_string)

                return (
                    jsonify({"message": "success", "redirect_url": f"/group/{gid}"}),
                    200,
                )

            except Exception as e:
                print(f"エラーが発生しています：{e}")
                abort(500)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error/404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error/500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
