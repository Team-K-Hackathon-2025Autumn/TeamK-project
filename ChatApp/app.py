from flask import (
    Flask,
    request,
    redirect,
    render_template,
    session,
    flash,
    abort,
    url_for,
)
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import User, Group, Member, Message
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


# ログインページ表示
@app.route("/login", methods=["GET"])
def login_view():
    uid = session.get("uid")
    if uid is None:
        return render_template("auth/login.html")
    return redirect(
        url_for("home_view")
    )  # ログイン済みの場合、グループ一覧にリダイレクト


# グループ一覧ページ表示
@app.route("/home", methods=["GET"])
def home_view():
    uid = session.get("uid")
    if uid is None:
        return render_template("auth/login.html")
    else:
        groups = Group.get_all()
        groups.reverse()
        return render_template("home.html", groups=groups, uid=uid)


# グループ名編集
@app.route("/group/<gid>/update", methods=["POST"])
def update_group(gid):
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    else:
        new_group_name = request.form.get("groupName")
        Group.update(gid, new_group_name)
        return redirect("/group/{gid}")


# グループ削除
@app.route("/group/<gid>/delete", methods=["POST"])
def delete_group(gid):
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    else:
        group = Group.find_by_gid(gid)
        if gid != group["gid"]:
            flash("グループは作成者のみ削除可能です")
        else:
            Group.delete(gid)

        return redirect("home_view")
