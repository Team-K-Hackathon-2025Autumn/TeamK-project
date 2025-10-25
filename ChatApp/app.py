# メッセージ一覧ページ表示（各グループ内で、そのグループに属している全メッセージを表示させる）
@app.route("/group/<gid>", methods=["GET"])
def message_view(gid):
    uid = session.get("uid")
    if uid is None:
        return redirect(url_for("login_view"))
    else:
        group = Group.find_by_gid(gid)
        messages = Message.get_all(gid)
        members = Member.get_all(gid)
        return render_template(
            "group/messages.html",
            messages=messages,
            group=group,
            members=members,
            uid=uid,
        )
