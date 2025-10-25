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
