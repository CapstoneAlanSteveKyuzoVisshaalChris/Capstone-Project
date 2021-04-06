import requests
import json

#Constants
AI_URL = "http://127.0.0.1:5000/"
HEADER = {"Content-Type": "application/json"}

def default_tezt():
    url = AI_URL
    header = HEADER
    data = json.dumps({
        "username": "Adam&Steve",
        "pref_data": [ "nature" ]
    })
    resp = requests.post(url, headers=header, data=data)

    json_blob = resp.json()
    return json_blob

def unraw_tezt():
    url = AI_URL
    header = HEADER
    data = json.dumps({
        "username": "Adam&Steve",
        "raw" : False,
        "pref_data": [ "nature", "trees" ]
    })
    resp = requests.post(url, headers=header, data=data)

    json_blob = resp.json()
    return json_blob

def raw_tezt():
    url = AI_URL
    header = HEADER
    data = json.dumps({
        "username": "Boxwell",
        "raw" : True,
        "pref_data": [ "nature", "flowers" ]
    })
    resp = requests.post(url, headers=header, data=data)

    json_blob = resp.json()
    return json_blob

if __name__ == "__main__":
    print(default_tezt())
    print(unraw_tezt())
    print(raw_tezt())