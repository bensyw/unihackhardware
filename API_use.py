#!/usr/bin/python3

import requests
import base64
from requests.auth import HTTPBasicAuth
import json


user = 'demo1'
password = 'hackathon7493'
json_headers = {
    'Content-Type': 'application/json',
}

# print(data)

# post_call = requests.post('http://smartvision.aiam-dh.com:8080/api/v1.0/tasks',
#                           headers=headers, data=data, auth=HTTPBasicAuth('demo1', 'hackathon7493'))


# input is the path to the image
def upload_image(image_path):
    with open("aussie.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        data_send = '{"service":"tagging1","image":"' + encoded_string.decode() + """ "}"""
        post_call = requests.post('http://smartvision.aiam-dh.com:8080/api/v1.0/tasks', headers=json_headers, data=data_send, auth=HTTPBasicAuth(user, password))
        # print out debug info
        # print(post_call, "POST call")
        # print(post_call.text, "TEXT")
        # print(post_call.content, "CONTENT")
        # print(post_call.status_code, "STATUS CODE")


def GetInfoImage():
        # Don't need to implement if we only process one image at a time
    pass


def GetInfoAll():
    get_call = requests.get('http://smartvision.aiam-dh.com:8080/api/v1.0/tasks', headers=json_headers, auth=HTTPBasicAuth(user, password))
    print(get_call.text, "TEXT")
    return json.loads(get_call.text)

def PutUpdate():
    pass


def PutRun():
    pass


def Delete():
    import requests

requests.delete('http://smartvision.aiam-dh.com:8080/api/v1.0/tasks/123', headers=headers, auth=('usr', 'pwd'))
    pass

if __name__ == "__main__":
    data = GetInfoAll()
    print(data)
