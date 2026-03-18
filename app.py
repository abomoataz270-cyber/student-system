import requests
from PyQt5.QtWidgets import QMessageBox

# دالة الاتصال بالسيرفر
def login_online(username, key):
    try:
        res = requests.post(
            "http://127.0.0.1:5000/login",
            json={"username": username, "key": key}
        )
        return res.json()["status"]
    except:
        return "error"
 
 def check_login(self):
    user = self.username.text()
    key = self.password.text()

    status = login_online(user, key)

    if status == "success":
        self.accept()
    elif status == "expired":
        QMessageBox.warning(self, "انتهى", "الاشتراك منتهي ❌")
    elif status == "fail":
        QMessageBox.warning(self, "خطأ", "بيانات غير صحيحة ❌")
    else:
        QMessageBox.warning(self, "خطأ", "مشكلة في الاتصال بالسيرفر 🌐")
 