from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
import hashlib
import uuid
import re
import os


# from models import User, Post, Comment
# temp 
from models import User, Post#, Comment, Follow, Bookmark

# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

csrf = CSRFProtect(app)

# ルートページのリダイレクト処理
@app.route('/', methods=['GET'])
def index():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))
    return redirect(url_for('posts_view'))


# サインアップページの表示
@app.route('/signup', methods=['GET'])
def signup():
    if session.get('user_id') is not None:
        return redirect(url_for('posts_view'))
    return render_template('auth/signup.html')


# サインアップ処理
@app.route('/signup', methods=['POST'])
def signup_process():
    print('Signup process started') # Debug

    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    password_confirmation = request.form.get('password_confirmation', '')

    # 空チェック
    if not name or not email or not password or not password_confirmation:
        flash("空のフォームがあります" , 'error')
        return redirect(url_for('signup'))

    # パスワード一致チェック
    if password != password_confirmation:
        flash('二つのパスワードの値が違っています','error')
        return redirect(url_for('signup'))

    # メール形式チェック
    if re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式ではありません','error')
        return redirect(url_for('signup'))

    # 既存ユーザーチェック
    registered_user = User.find_by_email(email)
    if registered_user is not None:
        flash('既に登録されているメールアドレスです','error')
        return redirect(url_for('signup'))

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    user_id = User.create(name, email, hashed_password)

    session['user_id'] = user_id

    return redirect(url_for('posts_view'))


# ログインページの表示
@app.route('/login', methods=['GET'])
def login():
    if session.get('user_id') is not None:
        return redirect(url_for('posts_view'))
    return render_template('auth/login.html')


# ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    if email =='' or password == '':
        flash('メールアドレスorパスワードが空です','error')
    else:
        user = User.find_by_email(email)
        if user is None:
            flash('メールアドレスorパスワードが違います','error')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('メールアドレスorパスワードが違います','error')
            else:
                session['user_id'] = user["user_id"]
                return redirect(url_for('posts_view'))
    return redirect(url_for('login'))


# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# 投稿一覧ページの表示
@app.route('/posts', methods=['GET'])
def posts_view():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))
    else:
        posts = Post.get_all()
        for post in posts:
            post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M')
            post['user_name'] = User.get_name_by_id(post['user_id'])

        return render_template('post/posts.html', posts=posts, user_id=user_id)


# 投稿処理
@app.route('/posts', methods=['POST'])
def create_post():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))
    content = request.form.get('content', '').strip()
    if content == '':
        flash('投稿内容が空です','error')
        return redirect(url_for('posts_view'))
    Post.create(user_id, content)
    flash('投稿が完了しました','success')
    return redirect(url_for('posts_view'))

# 投稿削除処理
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))

    post = Post.find_by_id(post_id)
    if post is None:
        abort(404)

    if post['user_id'] != user_id:
        flash('この投稿を削除することはできません', 'error')
        return redirect(url_for('posts_view'))

    Post.delete(post_id)
    flash('投稿が削除されました','success')
    return redirect(url_for('posts_view'))

# 投稿詳細ページの表示
@app.route('/posts/<int:post_id>', methods=['GET'])
def post_detail_view(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))
    post = Post.find_by_id(post_id)
    if post is None:
        abort(404)
    post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M')
    post['user_name'] = User.get_name_by_id(post['user_id'])

    comments = Comment.get_by_post_id(post_id)
    for comment in comments:
        comment['created_at'] = comment['created_at'].strftime('%Y-%m-%d %H:%M')
        comment['user_name'] = User.get_name_by_id(comment['user_id'])

    return render_template('post/post_detail.html', post=post, comments = comments, user_id=user_id)

# コメント処理
@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))
    content = request.form.get('content', '').strip()
    if content == '':
        flash('コメント内容が空です','error')
        return redirect(url_for('post_detail_view', post_id=post_id))
    Comment.create(user_id, post_id, content)
    flash('コメントの投稿が完了しました','success')
    return redirect(url_for('post_detail_view', post_id=post_id))

# コメント削除機能
@app.route('/comments/<int:comment_id>/delete', methods=['POST']) # 削除時はPOSTメソッドを使う
def delete_comment(comment_id): # comment_idを引数に渡しメソッドでコメントを探す時user_idに紐づいた
    user_id = session.get('user_id') # ログインチェック
    if user_id is None:
        return redirect(url_for('login_view'))

    comment = Comment.find_by_id(comment_id) # コメントの存在チェック
    if comment is None:
        abort(404) # コメントが見つからなければ404エラー

    # 権限チェック: ログインユーザーがコメントの投稿者であるか
    if comment['user_id'] != user_id:
        flash('このコメントを削除することはできません', 'error')
        # どこにリダイレクトするかは、コメントが削除される前のページ（例: 投稿詳細ページ）が良い
        return redirect(url_for('post_detail_view', post_id=comment['post_id']))

    Comment.delete(comment_id) # コメントの削除
    flash('コメントが削除されました','success')
    return redirect(url_for('post_detail_view', post_id=comment['post_id'])) # 投稿詳細ページにリダイレクト

@app.route('/profile', methods=['GET'])
def profile_view():
    user_id = session.get('user_id') # ここでセッションからuser_idを取得
    if user_id is None: # ログインしてないなら
        return redirect(url_for('login')) # ログイン画面に飛ばす
    user = User.find_by_id(user_id) # user変数にUserテーブルから(user_id)ログインしてるユーザと同じIDのデータを代入する。
    return render_template('profile/profile.html', user=user) # テンプレートフォルダを探しその中のprofileディレクトリ内の指定したhtmlを読み込みuser変数の情報をhtml内でuserという名前で使える

@app.route('/myposts', methods=['GET'])
def myposts_view():
    user_id = session.get('user_id') # ここでセッションからuser_idを取得
    if user_id is None:
        return redirect(url_for('login'))
    # ここにuser_idの投稿を取得し新着順に羅列するロジック
    posts = Post.get_by_user_id(user_id) # posts変数にPostテーブルから(user_id)ログインしてるユーザと同じIDのデータを代入する。
    for post in posts:
        post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M')# for文処理がないと/postsと同じ表示にならない
    return render_template('post/myposts.html', myposts=posts) # テンプレートフォルダ内のpostディレクトリ配下のmypost.htmlを読み込みposts変数の情報をhtml内でmypostsという名前で使える

# ブックマーク機能
@app.route('/bookmark', methods=['GET'])
def my_bookmark():
    user_id = session.get('user_id') # ここでセッションからuser_idを取得
    if user_id is None: # ログインしてないなら
        return redirect(url_for('login_view')) # ログイン画面に飛ばす
    bookmark_records = Bookmark.get_by_user_id(user_id)# ブックマークをレコード('bookmark_id': 1,user_id: 3,post_id: 1)で管理する。その情報を bookmark_recordsに代入する。
    bookmarked_posts = []#レコードの入れ物を作成する。
    for record in bookmark_records:
        # 各ブックマークレコードからpost_idを取得し、Postテーブルから投稿の詳細を取得
        post = Post.find_by_id(record['post_id'])
        # if postでpostが存在してるかを問い、post.get('deleted_at') is None:でdeleted_atカラムがnull (未削除) であることを確認
        if post and post.get('deleted_at') is None: # post.get('deleted_at')でdeleted_atカラムの値を取得
            post['created_at'] = post['created_at'].strftime('%Y-%m-%d %H:%M') # 日付の整形
            bookmarked_posts.append(post) # 整形した投稿情報をリストに追加
    # テンプレートに整形済みの投稿リストを渡す
    return render_template('auth/bookmark.html', my_bookmarks=bookmarked_posts, user_id=user_id)

# フォロワー一覧画面
@app.route('/followers', methods=['GET'])
def my_followers():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))

    # 1. ログインユーザーがフォローしているユーザーのリストを取得
    following_users = Follow.get_following_users(user_id) # models.pyのメソッド[get_following_users]を呼び出しfollowing_usersに代入する。
#get_following_usersはログインユーザがフォローしているユーザのfollow_idに紐づいたIDをuserテーブルから取得する
    # 2. ログインユーザーをフォローしているユーザーのリストを取得
    followers_of_user = Follow.get_followers_of_user(user_id) # models.pyのメソッドを呼び出しfollowers_of_userに代入する。
#get_followers_of_userはログインユーザをフォローしているユーザの一覧を返す。
    # 必要であれば、ここで取得したユーザーリストの整形（例: 日付フォーマットは不要だが、表示名など）を行う

    # テンプレートに両方のリストを渡す
    return render_template(
        'auth/followers.html', # テンプレートのパスは適宜調整
        following_users=following_users, # 自分がフォローしている人たち
        followers_of_user=followers_of_user, # 自分をフォローしている人たち
        user_id=user_id # ログインユーザーのID
    )

@app.errorhandler(400)
def bad_request(error):
    return render_template('error/400.html'), 400

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'),404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html'),500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)