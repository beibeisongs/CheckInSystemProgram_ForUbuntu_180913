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
#   First: curl http://120.79.132.142/student/create_space/123456/20171000718
#   Second: run the script named "Client.py"
