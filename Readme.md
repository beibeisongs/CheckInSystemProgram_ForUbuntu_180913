# Attention:
#   When testing the script hello.py on Windows 10 Platfrom's CMD
#   Please use the following IP, through Pycharm shows Running on http://0.0.0.0:5001/
#       curl http://127.0.0.1:5001/
#   Then the response will be "welcome"

# Attention:    The Notes of setting up this Program
#   First, create an document named "student_photo" in location "/var/www/demoapp/"
#   Second, create the empty file "log.txt"
#       It ll only used while debugging process
#       Remember to delete the relative scripts such as log_file.write()
#       In order that No errors appear when using in the real time
#   Other INFO:
#       "student_photo" is used in the script named "hello.py", which stores students'photo when sign up their Accounts

# Attention:    Different Variables recording:
#   First: Ultimate sign up photo name and directory sample:
#       /var/www/demoapp/123456/20171000719/123456_20171000719_signup_1.jpg

# Attention:    Testing Program Steps:
#   First: curl http://120.79.132.142/student/create_space/123456/20171000720
#   Second: run the script named "Client.py"

#   First: curl http://120.79.132.142/student/create_space/123456/20171000719
#   Second: run the script named "Client.py"

# ----------------------------------------------------------------------------------------------------------------------
# Attention:
#   The following description is the testing process records
#   First:
#       run the script: Client_1.py
#                           using the request order of :
#                               r = requests.post("http://120.79.132.142/sign_up_photo_upload", data=user_info, files=files)
#   Second:
#       run the script: Client_1.py
#                           using the request order of :
#                               r = requests.post("http://120.79.132.142/checkin_photo_upload1", data=user_info, files=files)
#   Third:
#       run the script: Client_1.py
#                           using the request order of :
#                               r = requests.post("http://120.79.132.142/checkin_photo_upload2", data=user_info, files=files)
#   Fourth:
#       run the script: Client_1.py
#                           using the request order of :
#                               r = requests.post("http://120.79.132.142/post_function_test1", data=user_info)
#   Fifth:
#       run the script: Client_1.py
#                           using the request order of :
#                               r = requests.post("http://120.79.132.142/student_create_space", data=json.dumps(user_info))
#   Sixth:
#       run the script: Client_1.py
#                           using the request order of :
#                               r = requests.post("http://120.79.132.142/sign_up_photo_upload/123456/20171000721", files=files)
#   Seventh:
#       run the script: Client_1.py
#                           using the request order of :
#                               r = requests.post("http://120.79.132.142/route_data_upload/123456/20171000721/456/123/new")
#   Eighth:
#       run the script: Client_1.py
#                           using the request order of :
#                               r = requests.post("http://120.79.132.142/route_data_upload/123456/20171000721/456/123/middle")
#   Nineth:
#       run the script: Client_1.py
#                           using the request order of :
#                               r = requests.post("http://120.79.132.142/route_data_upload/123456/20171000721/456/123/end")
#   Make a small api-conclusion:
#
#   r = requests.post("http://120.79.132.142/student_create_space", data=json.dumps(user_info))
#   r = requests.post("http://120.79.132.142/sign_up_photo_upload/123456/20171000721", files=files)
#   r = requests.post("http://120.79.132.142/checkin_photo_upload1", data=user_info, files=files)
#   r = requests.post("http://120.79.132.142/checkin_photo_upload2", data=user_info, files=files)
#   r = requests.post("http://120.79.132.142/route_data_upload/123456/20171000721/456/123/new")
#   r = requests.post("http://120.79.132.142/route_data_upload/123456/20171000721/456/123/middle")
#   r = requests.post("http://120.79.132.142/route_data_upload/123456/20171000721/456/123/end")
