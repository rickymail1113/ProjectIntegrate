from flask import Flask, render_template, request, redirect
from datetime import datetime
import time



app = Flask(__name__)


class Guest:
    def __init__(self, uid, name, contact):
        self.uid = uid
        self.name = name
        self. contact = contact

count = 0
DB = []


@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    if "POST" == request.method:
        if 0 < len(request.form.get("uname")) and 0 < len(request.form.get("contact")):
            unix_num = int(datetime.now().timestamp())
            DB.append(Guest(unix_num, request.form.get("uname"), request.form.get("contact")))

    return render_template("index.html", db=DB)


@app.route("/add_user")
def add_user():
    return render_template("add_user.html")


@app.route("/edit_user")
@app.route("/edit_user/<int:uid>")
def edit_user(uid):
    for i in DB:
        if uid == i.uid:
            return render_template("edit_user.html", data=i)

    return render_template("index.html", db=DB)


@app.route("/user_edited/<int:uid>", methods=["POST"])
def user_edited(uid):
    for i in DB:
        if uid == i.uid:
            i.name = request.form.get("uname")
            i.contact = request.form.get("contact")
            break

    return render_template("index.html", db=DB)


@app.route("/user_delete/<int:uid>")
def user_delete(uid):
    for i in DB:
        if uid == i.uid:
            DB.remove(i)
            break

    # return render_template("index.html", db=DB)

    # 請客戶端瀏覽器重新導向指定頁面
    return redirect("/index")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)