from flask import Flask, redirect ,render_template, session, flash, url_for


app = Flask(__name__)

@app.route("/")
def index():
    # ここは login を見せたいなら login に飛ばすのもアリ
    return render_template("post/base.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template("auth/login.html")

@app.route("/signup", methods=["GET"])
def signup():
    return render_template("auth/signup.html")

@app.route("/profile",methods=["GET"])
def profile():
    return render_template("auth/profile.html")

if __name__ == "__main__":
    app.run(debug=True)
