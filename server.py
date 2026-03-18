from flask import Flask, request, jsonify, render_template_string
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

FILE = "users.xlsx"

# إنشاء ملف Excel لو مش موجود
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["username", "key", "expire"])
    df.to_excel(FILE, index=False)

# ===== تسجيل الدخول =====
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    df = pd.read_excel(FILE)

    user = df[df["username"] == data["username"]]

    if not user.empty:
        if user.iloc[0]["key"] == data["key"]:
            expire = datetime.strptime(str(user.iloc[0]["expire"]), "%Y-%m-%d")
            if datetime.now() < expire:
                return jsonify({"status": "success"})
            else:
                return jsonify({"status": "expired"})

    return jsonify({"status": "fail"})

# ===== لوحة التحكم =====
@app.route("/", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form["username"]
        key = request.form["key"]
        expire = request.form["expire"]

        df = pd.read_excel(FILE)

        # حذف المستخدم القديم
        df = df[df["username"] != username]

        # إضافة الجديد
        new_row = pd.DataFrame([[username, key, expire]],
                               columns=["username", "key", "expire"])

        df = pd.concat([df, new_row])

        df.to_excel(FILE, index=False)

    df = pd.read_excel(FILE)

    return render_template_string("""
    <h2>Admin Panel</h2>

    <form method="post">
        <input name="username" placeholder="username"><br>
        <input name="key" placeholder="key"><br>
        <input name="expire" placeholder="2026-12-31"><br>
        <button>Save</button>
    </form>

    <hr>
    {{table|safe}}
    """, table=df.to_html())

if __name__ == "__main__":
    app.run()
