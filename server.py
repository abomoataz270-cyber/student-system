from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

FILE = "users.xlsx"

# إنشاء ملف Excel لو مش موجود
def create_file():
    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=["username", "key", "expiry"])
        df.to_excel(FILE, index=False)

# قراءة البيانات
def read_users():
    create_file()
    try:
        return pd.read_excel(FILE)
    except:
        return pd.DataFrame(columns=["username", "key", "expiry"])

# الصفحة الرئيسية
@app.route("/")
def home():
    return "Server is running ✅"

# تسجيل الدخول
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        username = data.get("username")
        key = data.get("key")

        if not username or not key:
            return jsonify({"status": "error", "message": "missing data"})

        df = read_users()

       user = df[
    (df["username"].astype(str).str.strip() == str(username).strip()) &
    (df["key"].astype(str).str.strip() == str(key).strip())
]
        if user.empty:
            return jsonify({"status": "fail"})

        expiry = pd.to_datetime(user.iloc[0]["expiry"])

        if expiry < datetime.now():
            return jsonify({"status": "expired"})

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})