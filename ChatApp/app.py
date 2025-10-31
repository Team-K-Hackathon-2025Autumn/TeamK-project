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

# -----　ここから下が新規アップロード分 -----

# ユーザー新規登録処理(b-5)Masa担当
@app.route('/signup', methods = ['POST'])
def signup_process():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    passwordConfirmation = request.form.get('passwordConfirmation')

    if name == '' or email == '' or password == '' or passwordConfirmation == '':
        flash('空のフォームがあります')
    elif password != passwordConfirmation:
        flash('二つのパスワードが一致しません')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('メールアドレスが正しくありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        registered_user = User.find_by_email(email)

        if registered_user != None: 
            flash('メールアドレスがすでに登録されています')
        else:
            User.create(uid, name, email, password)
            UserID = str(uid)
            session['uid'] = UserID
            return redirect(url_for('home_view'))
    return redirect(url_for('signup_view'))