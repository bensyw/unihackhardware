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


def get_info_image():
    # Don't need to implement if we only process one image at a time
    pass


def get_info_all():
    """
    :return: all json format HTTP response
    """
    get_call = requests.get('http://smartvision.aiam-dh.com:8080/api/v1.0/tasks',
                            headers=json_headers, auth=(user, password))
    print(get_call.text, "TEXT")
    return json.loads(get_call.text)


def update_image():
    pass

# return dict format
# "task": {
#  "description": "Milk, Cheese ",
#  "confidence": "80,90",
#  "location": "70,80,100,110",
#  "scanned": true,
#  "uploaded": true,
#  "id": 2,
#  "userid": 2,
#  "service": "azure1"
#  },
def run_recog(id_name):
    data = '{"scanned": true}'
    response = requests.put('http://smartvision.aiam-dh.com:8080/api/v1.0/tasks/run/' + str(id_name),
                 headers=json_headers, data=data, auth=(user, password))
    return json.loads(response.text)



def delete(id_name):
    """
    delete the upload image that correspond to the unique id
    :param id_name: unique number that match a upload image
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


def get_all_list():
    """
    function get all unique ids from API and return them
    :return:  all unique ids
    """
    jsonreturned = get_info_all()
    tasks_dict = jsonreturned['tasks']
    upload_ids = [field["uri"] for field in tasks_dict]
    result = []
    for teststr in upload_ids:
        testint = int(teststr.replace(
            'http://smartvision.aiam-dh.com:8080/api/v1.0/tasks/', ''))
        result.append(testint)
    return result


def initialize():
    """
    delete all cached tasks
    :return: if there are thing is side API website return True, otherwise False
    """
    if len(get_all_list()):
        for id_name in get_all_list():
            delete(id_name)
        return True
    else:
        return False


if __name__ == "__main__":
    # a = upload_image("aussie.jpg")
    # print(a)
    data = get_info_all()
    print(data)

    initialize()

    #ListofUploadIds = GetAllList()
    #print(ListofUploadIds)
