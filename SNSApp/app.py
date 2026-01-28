from flask import Flask, redirect ,render_template, session, flash, url_for


app = Flask(__name__)

@app.route("/")
def index():
    # ここは login を見せたいなら login に飛ばすのもアリ
    return render_template("base.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template("auth/login.html")

@app.route("/signup", methods=["GET"])
def signup():
    return render_template("auth/signup.html")


@app.route("/posts", methods=["GET"])
def posts():
    return render_template("post/posts.html")

@app.route("/post_detail", methods=["GET"])
def post_detail():
    return render_template("post/post_detail.html")


@app.route("/profile",methods=["GET"])
def profile():
    return render_template("auth/profile.html")

@app.route("/mypage",methods=["GET"])
def mypage():
    return render_template("auth/mypage.html")

@app.route("/bookmark",methods=["GET"])
def bookmark():
    return render_template("auth/bookmark.html")

@app.route("/followers",methods=["GET"])
def followers():
    return render_template("auth/followers.html")
if __name__ == "__main__":
    app.run(debug=True)
