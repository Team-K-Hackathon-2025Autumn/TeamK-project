# ログイン処理
from flask import flash, session

@app.route("/login", methods=["POST"])## ログインページでPOSTリクエストが来た場合
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
                session["uid"] = user["uid"]
                return redirect(url_for("channnels_view"))
        return redirect(url_for("login_view"))
    