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
