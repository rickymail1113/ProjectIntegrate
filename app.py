from flask import Flask, render_template, request, redirect, flash, url_for, session
from datetime import datetime
import time
import database

app = Flask(__name__)


class Guest:
    def __init__(self, uid, name, content):
        self.uid = uid
        self.name = name
        self. content = content

count = 0
DB = []


@app.route("/")
@app.route("/index")
def index():
    print(database.query_datas())
    return render_template("index.html", db=database.query_datas())


@app.route("/add_user")
def add_user():
    return render_template("add_user.html")


@app.route("/user_add", methods=["POST"])
def user_add():
    if 0 < len(request.form.get("uname")) and 0 < len(request.form.get("content")):
        unix_num = int(datetime.now().timestamp())
        database.insert_data(request.form.get("uname"), request.form.get("content"))
        flash("新增成功")

    return redirect(url_for('index'))


@app.route("/edit_user/<int:uid>")
def edit_user(uid):
    if 0 < uid:
        data = database.find_data(uid)
        if None != data:
            return render_template("edit_user.html", data=Guest(data[0], data[1], data[2]))

    return redirect(url_for('index'))


@app.route("/user_edited/<int:uid>", methods=["POST"])
def user_edited(uid):
    if 0 < uid:
        data = database.update_data(uid, request.form.get("uname"), request.form.get("content"))

    return redirect(url_for('index'))


@app.route("/user_delete/<int:uid>")
def user_delete(uid):
    if 0 < uid:
        data = database.delete_data(uid)

    # 請客戶端瀏覽器重新導向指定頁面
    return redirect("/index")


@app.route('/session/')
def session_index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'


@app.route('/session/login/', methods=['GET', 'POST'])
def session_login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('session_index'))
    return '''
        <form method="post">
            <p>帳號<input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/session/logout/')
def session_logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('session_index'))


if __name__ == "__main__":
    app.secret_key="123456789"
    app.run(host="0.0.0.0", port=8080, debug=True)