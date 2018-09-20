# encoding=utf-8
# Date: 2018-09-13
# Author: MJUZY


import requests


if __name__ == "__main__":

    # files = {'image01': open('D:\\PyFlaskLearningProjects\\20180613_Test1\\Client\\01.jpg', 'rb')}
    # user_info = {'name': 'letian'}
    # r = requests.post("http://127.0.0.1:5001/upload", data=user_info, files=files)

    # files = {'image01': open('/var/www/demoapp/01.jpg', 'rb')}
    # user_info = {'name': 'letian'}
    # r = requests.post("http://0.0.0.0:5001/upload", data=user_info, files=files)

    files = {'image01': open('./kkk.jpg', 'rb')}
    user_info = {'class_name': '123456', 'name': '20171000716'}

    # r = requests.post("http://120.79.132.142:5001/upload", data=user_info, files=files)
    # The Codes upside used for Windows to upload file to Ubuntu, but not passed !
    # The Codes below used for Windows, and proved correct !
    # r = requests.get("http://120.79.132.142")
    # The Codes below used for Windows to upload file to Ubuntu, and proved Correct !

    """r = requests.post("http://120.79.132.142/sign_up_photo_upload", data=user_info, files=files)"""
    r = requests.post("http://120.79.132.142/checkin_photo_upload2", data=user_info, files=files)
    """r = requests.post("http://120.79.132.142/checkin_photo_upload2", data=user_info, files=files)"""

    print(r.text)
