#!/usr/bin/python3

import requests
import base64
from requests.auth import HTTPBasicAuth

with open("aussie.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    # print(encoded_string)

headers = {
    'Content-Type': 'application/json',
}


data = '{"service":"tagging1","image":"' + encoded_string.decode() + """ "}"""
# print(data)

# post_call = requests.post('http://smartvision.aiam-dh.com:8080/api/v1.0/tasks',
#                           headers=headers, data=data, auth=HTTPBasicAuth('demo1', 'hackathon7493'))


def PostImage():
    post_call = requests.post('http://smartvision.aiam-dh.com:8080/api/v1.0/tasks',
                              headers=headers, data=data, auth=HTTPBasicAuth('demo1', 'hackathon7493'))
    print(post_call, "POST call")
    print(post_call.text, "TEXT")
    print(post_call.content, "CONTENT")
    print(post_call.status_code, "STATUS CODE")


def GetInfoImage():
        # Don't need to implement if we only process one image at a time
    pass


def GetInfoAll():
    get_call = requests.get('http://smartvision.aiam-dh.com:8080/api/v1.0/tasks',
                            headers=headers, auth=HTTPBasicAuth('demo1', 'hackathon7493'))


def PutUpdate():
    pass


def PutRun():
    pass


def Delete():
    pass
