# encoding=utf-8
# Date: 2018-09-13
# Author: MJUZY


import base64
import cv2
import skimage.io as io
import json
import numpy as np
import requests

if __name__ == "__main__":
    with open("kkk.jpeg", 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode("utf-8")

    user_info = {'class_name': '117171', 'name': '20171002196', "image01": s}

    # r = requests.post("http://120.79.132.142:5001/upload", data=user_info, files=files)
    # The Codes upside used for Windows to upload file to Ubuntu, but not passed !
    # The Codes below used for Windows, and proved correct !
    # r = requests.get("http://120.79.132.142")
    # The Codes below used for Windows to upload file to Ubuntu, and proved Correct !

    # r = requests.post("http://120.79.132.142/post_function_test1", data=user_info)"""
    # r = requests.post("http://120.79.132.142/student_create_space", json=user_info)
    # r = requests.post("http://120.79.132.142/sign_up_photo_upload", data=user_info, files=files)

    """ Description: 

        The samples following is the conclusion of api-s that are useful
    """
    # r = requests.post("http://120.79.132.142/student_create_space", data=json.dumps(user_info))
    r = requests.post("http://120.79.132.142/sign_up_photo_upload_base64/117171/20171002196", data=user_info)

    """r = requests.post("http://120.79.132.142/checkin_photo_upload1", data=user_info, files=files)"""
    """r = requests.post("http://120.79.132.142/checkin_photo_upload2", data=user_info, files=files)"""
    # r = requests.post("http://120.79.132.142/route_data_upload/123456/20171000721/456/123/new")
    # r = requests.post("http://120.79.132.142/route_data_upload/123456/20171000721/456/123/middle")
    # r = requests.post("http://120.79.132.142/route_data_upload/123456/20171000721/456/123/end")

    print(r.text)
