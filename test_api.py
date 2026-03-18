import requests

url = "https://student-system-production-xxxx.up.railway.app/login"

data = {
    "username": "admin",
    "key": "1234"
}

res = requests.post(url, json=data)

print(res.json())