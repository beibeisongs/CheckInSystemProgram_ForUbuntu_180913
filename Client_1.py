# encoding=utf-8
# Date: 2018-09-13
# Author: MJUZY


import json
import requests


if __name__ == "__main__":

    files = {'image01': open('./kkk.jpg', 'rb')}

    user_info = {'class_name': '123456', 'name': '20171000721'}

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
    # r = requests.post("http://120.79.132.142/sign_up_photo_upload/123456/20171000721", files=files)
    """r = requests.post("http://120.79.132.142/checkin_photo_upload1", data=user_info, files=files)"""
    """r = requests.post("http://120.79.132.142/checkin_photo_upload2", data=user_info, files=files)"""
    # r = requests.post("http://120.79.132.142/route_data_upload/123456/20171000721/456/123/new")
    # r = requests.post("http://120.79.132.142/route_data_upload/123456/20171000721/456/123/middle")
    r = requests.post("http://120.79.132.142/route_data_upload/123456/20171000721/456/123/end")

    print(r.text)
