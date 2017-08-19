#!/usr/bin/python3

import requests
import base64
import re
import json


user = 'demo1'
password = 'hackathon7493'
json_headers = {
    'Content-Type': 'application/json',
}

# print(data)

# post_call = requests.post('http://smartvision.aiam-dh.com:8080/api/v1.0/tasks',
#                           headers=headers, data=data, auth=HTTPBasicAuth('demo1', 'hackathon7493'))


def upload_image(image_path):
    """
    upload image to API
    :param image_path: the path to the file
    :return: unique id number for the upload image, else return false
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        data_send = '{"service":"tagging1","image":"' + \
            encoded_string.decode() + """ "}"""
        post_call = requests.post('http://smartvision.aiam-dh.com:8080/api/v1.0/tasks',
                                  headers=json_headers, data=data_send, auth=(user, password))
        # print out debug info
        print(post_call, "POST call")
        print(post_call.text, "TEXT")
        print(post_call.content, "CONTENT")
        print(post_call.status_code, "STATUS CODE")
        print(type(post_call.status_code))

        response_json = json.loads(post_call.text)

        if 'task' in response_json:
            if 'uri' in response_json['task']:
                return response_json['task']['uri'].split('/')[-1]
            else:
                return False
        else:
            return False


def GetInfoImage():
    # Don't need to implement if we only process one image at a time
    pass


def GetInfoAll():
    get_call = requests.get('http://smartvision.aiam-dh.com:8080/api/v1.0/tasks',
                            headers=json_headers, auth=(user, password))
    print(get_call.text, "TEXT")
    return json.loads(get_call.text)


def PutUpdate():
    pass


def PutRun():
    pass


def Delete(id_name):
    """
    delete the upload image that correspond to the unique id
    :param id: unique number that match a upload image
    :return: True if delete correctly, false if delete unsuccessfully, or the id number doesn't exist
    """
    response = requests.delete('http://smartvision.aiam-dh.com:8080/api/v1.0/tasks/' + str(id_name), headers=json_headers, auth=(user, password))
    response_json = json.loads(response.text)
    if 'result' in response_json:
        if response_json['result']:
            return True
        else:
            return False
    else:
        return False


def GetAllList():
    jsonreturned = GetInfoAll()
    tasks_dict = jsonreturned['tasks']
    upload_ids = [field["uri"] for field in tasks_dict]
    result = []
    for teststr in upload_ids:
        testint = int(teststr.replace(
            'http://smartvision.aiam-dh.com:8080/api/v1.0/tasks/', ''))
        result.append(testint)
    return result


def Initialize():
    if len(GetAllList()):
        for id in GetAllList():
            Delete(id)
        return True
    else:
        return False


if __name__ == "__main__":
    # a = upload_image("aussie.jpg")
    # print(a)
    data = GetInfoAll()
    print(data)

    Initialize()

    #ListofUploadIds = GetAllList()
    #print(ListofUploadIds)
