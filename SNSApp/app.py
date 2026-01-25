from flask import Flask, render_template

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


if __name__ == "__main__":
    app.run(debug=True)
