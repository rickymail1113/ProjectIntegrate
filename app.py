from flask import Flask, render_template, request, redirect, flash, url_for, session
from datetime import datetime
import time
import database
import requests
import os

app = Flask(__name__)


class Guest:
    def __init__(self, uid, name, content):
        self.uid = uid
        self.name = name
        self. content = content

count = 0
DB = []


AWS_DataBase = []

@app.route("/")
@app.route("/index")
# def index():
#     print(database.query_datas())
#     return render_template("index.html", db=database.query_datas())
def index():
     result = requests.post("https://h46cafa2f1.execute-api.ap-northeast-1.amazonaws.com/default/getStatus")
     AWS_DataBase.clear()
     for i in result.json():
         data = Guest(i['created'], i['status'], i['car_no'])
         AWS_DataBase.append(data)
     return render_template("index.html", db=AWS_DataBase)


@app.route("/add_user")
def add_user():
    return render_template("add_user.html")


@app.route("/user_add", methods=["POST"])
def user_add():
    # if 0 < len(request.form.get("uname")) and 0 < len(request.form.get("content")):
    #     unix_num = int(datetime.now().timestamp())
    #     database.insert_data(request.form.get("uname"), request.form.get("content"))
    #     flash("新增成功")
    file = request.files['filename']
    file.save(os.path.join(app.root_path, 'static', file.filename))
    filename = file.filename

    # 设置需要传输的二进制数据
    data = open('./static/' + filename, 'rb').read()

    # 设置请求头
    headers = {'Content-Type': 'application/octet-stream'}

    # 发送POST请求
    result = requests.post("https://h46cafa2f1.execute-api.ap-northeast-1.amazonaws.com/default/ImageUploadOCR",
                      data=data, headers=headers)
    print(result.json())

    flash("AWS判讀回覆!!")

    return redirect(url_for('index'))


@app.route("/edit_user/<int:uid>")
def edit_user(uid):
    if 0 < uid:
        # data = database.find_data(uid)
        for i in AWS_DataBase:
            print(i)
            if uid == i.uid:
                return render_template("edit_user.html", data=i)

    return redirect(url_for('index'))


@app.route("/user_edited/<int:uid>", methods=["POST"])
def user_edited(uid):
    if 0 < uid:
        # data = database.update_data(uid, request.form.get("uname"), request.form.get("content"))
        # 设置请求头

        data = {}
        for i in AWS_DataBase:
            print(i)
            if uid == i.uid:
                data = {'car_no': i.content, 'created': uid}
                break


        headers = {'Content-Type': 'application/json'}
        # 發送POST请求
        result = requests.post("https://h46cafa2f1.execute-api.ap-northeast-1.amazonaws.com/default/updateStatus",
                               json=data)
        print(request.base_url)
        print(result)

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