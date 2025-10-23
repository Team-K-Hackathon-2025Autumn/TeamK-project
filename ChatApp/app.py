# グループ一覧ページ表示
@app.route("/home", methods=["GET"])
def home_view():
    uid = session.get("uid")
    if uid is None:
        return render_template("auth/login.html")
    else:
        groups = Group.get_all()
        groups.reverse()
        return render_template("groups.html", groups=groups, uid=uid)
