import requests
import json

#Constants
AI_URL = "http://127.0.0.1:5000/"
HEADER = {"Content-Type": "application/json"}

def test1():
    url = AI_URL
    header = HEADER
    data = json.dumps({
        "keywords": [ "nature" ]
    })
    resp = requests.post(url, headers=header, data=data)

    json_blob = resp.json()
    return json_blob

def test2():
    url = AI_URL
    header = HEADER
    data = json.dumps({
        "keywords": [ "nature", "trees" ]
    })
    resp = requests.post(url, headers=header, data=data)

    json_blob = resp.json()
    return json_blob

def test3():
    url = AI_URL
    header = HEADER
    data = json.dumps({
        "keywords": [ "nature", "flowers" ]
    })
    resp = requests.post(url, headers=header, data=data)

    json_blob = resp.json()
    return json_blob

if __name__ == "__main__":
    print(test1())
    print(test2())
    print(test3())