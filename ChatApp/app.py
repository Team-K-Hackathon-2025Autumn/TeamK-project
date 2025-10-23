# ログインページ表示
@app.route("/login", methods=["GET"])
def login_view():
    uid = session.get("uid")
    if uid is None:
        return render_template("auth/login.html")
    return redirect(
        url_for("home_view")
    )  # ログイン済みの場合、グループ一覧にリダイレクト
