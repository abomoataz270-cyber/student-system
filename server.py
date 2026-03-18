from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

FILE = "users.xlsx"

# إنشاء الملف لو مش موجود
def create_file():
    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=["username", "key", "expiry"])
        df.to_excel(FILE, index=False)

# قراءة البيانات بأمان
def read_users():
    try:
        create_file()
        return pd.read_excel(FILE)
    except:
        return pd.DataFrame(columns=["username", "key", "expiry"])

# API تسجيل الدخول
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    key = data.get("key")

    df = read_users()

    user = df[(df["username"] == username) & (df["key"] == key)]

    if user.empty:
        return jsonify({"status": "fail"})

    expiry = pd.to_datetime(user.iloc[0]["expiry"])

    if expiry < datetime.now():
        return jsonify({"status": "expired"})

    return jsonify({"status": "success"})

# الصفحة الرئيسية
@app.route("/")
def home():
    return "Server is running ✅"

# تشغيل السيرفر
app = Flask(__name__)
