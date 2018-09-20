# encoding=utf-8
# Date: 2018-09-13
# Author: MJUZY


from extractMaxFace import extractProcess
from FaceRecognzedProcess import faceRecognzedProcess

import dlib
from flask import Flask, url_for
from flask import request
import shutil

from werkzeug.utils import secure_filename
import os

from werkzeug.contrib.cache import SimpleCache


app = Flask(__name__)

"""Descirption:
    When the FaceRecognition_Script Running
    We will use the document named CheckingAccounts
    To store the Accounts that are going to Statistic the Matched Faces
        Besides, we use name.txt to record the accounts' name
        
    When finishing Recognition Process
        the related txt file will be deleted 
"""
recogAssist_Dir = "/var/www/demoapp/CheckingAccounts"

if os.path.exists(recogAssist_Dir) == False:
    os.makedirs(recogAssist_Dir)

os.system("python /var/www/demoapp/Try_Function_2.py")


def prepare_detector(predictor_path, face_rec_model_path):
    file = open("/var/www/demoapp/show_hello_running.txt", 'a')
    file.write("Prepare_detector !\n")

    # 加载正脸检测器
    detector = dlib.get_frontal_face_detector()
    file.write("detector prepared !\n")

    # 加载人脸关键点检测器
    sp = dlib.shape_predictor(predictor_path)
    file.write("sp prepared !\n")

    # 加载人脸识别模型
    facerec = dlib.face_recognition_model_v1(face_rec_model_path)
    file.write("facerec prepared !\n")

    file.close()
    return detector, sp, facerec


def prepare_path_etc():
    # 人脸关键点检测器
    predictor_path = "/var/www/demoapp/shape_predictor_68_face_landmarks.dat"
    # 人脸识别模型：
    face_rec_model_path = "/var/www/demoapp/dlib_face_recognition_resnet_model_v1.dat"

    return predictor_path, face_rec_model_path


predictor_path, face_rec_model_path = prepare_path_etc()
detector, sp, facerec = prepare_detector(predictor_path, face_rec_model_path)

cache = SimpleCache()
cache.set("detector", detector)
cache.set("sp", sp)
cache.set("facerec", facerec)


# Method One: curl http://127.0.0.1:5000/hello?name=dongzheng
@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'


# Method Two/First: curl http://127.0.0.1:5000/articles/abc
# Output: You are reading abc
# Method Two/Second: curl http://127.0.0.1:5000/articles
# Output: List of /articles
@app.route('/')
def api_root():
    return 'Welcome'


@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')


@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid


# Method Three:
# C:\Users\zheng>curl -X Get http://127.0.0.1:5000/echo
# ECHO: GET
@app.route('/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"


# Method Four: see Client\__init__.py
# app.config['UPLOAD_FOLDER'] = 'D:\\PyFlaskLearningProjects\\20180613_Test1\\static\\uploads'
# The route below is used for Ubuntu, upside for Windows
app.config['UPLOAD_FOLDER'] = '/var/www/demoapp/student_photo'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/sign_up_photo_upload', methods=['POST'])
def upload():

    dirpath = '/var/www/demoapp'

    upload_file = request.files['image01']

    if upload_file and allowed_file(upload_file.filename):

        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))

        name = request.form.get('name', 'little apple')
        class_name = request.form.get('class_name', 'little apple')

        sign_up_photo_path = dirpath + "/student_photo/" + str(upload_file.filename)
        move_to_path = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "OriJPG"
        shutil.move(sign_up_photo_path, move_to_path)

        """Description: the orders following are used to check if the scripts have been correctly executed
        
        >>>log_file = open('/var/www/demoapp/log.txt', mode='a')
        >>>log_file.write("---shutil.move Ok !---")
        """

        IP = request.remote_addr

        """Face Extraction Part : 
        """
        dir = '/var/www/demoapp/Accounts'

        extractProcess(upload_file.filename, dir, class_name, name)

        return 'hello, ' + name + ' class_name: ' + class_name + 'IP : ' + IP + ' success'
    else:
        return 'hello, ' + request.form.get('name', 'little apple') + ' failed'


@app.route('/checkin_photo_upload', methods=['POST'])
def checkin_upload():
    """Attention:
        Now stipulate that Only Two Photos will be uploaded
    :return:
    """
    result = "This is the Original Value of the result !"

    detector_forcheckin = detector
    sp_forcheckin = sp
    facerec_forcheckin = facerec

    dir_path = '/var/www/demoapp/Accounts'

    upload_file = request.files['image01']

    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))

        name = request.form.get('name', 'little apple')
        class_name = request.form.get('class_name', 'little apple')

        dirpath_forcheckin = "/var/www/demoapp/student_photo"

        result = faceRecognzedProcess(detector_forcheckin, sp_forcheckin, facerec_forcheckin, dir_path, class_name, name, dirpath_forcheckin, upload_file.filename)

    return result


"""Sample:
    curl http://120.79.132.142/student/create_space/123456/20171000718
"""
@app.route('/student/create_space/<class_name>/<name>')
def api_create_space(class_name, name):

    new_path = "/var/www/demoapp/Accounts/" + class_name + "/" + name

    if os.path.exists(new_path) == False:
        os.makedirs(new_path)

        # Create the document storing CSV File, which used to recored customs' Travel coordinations
        new_csv_path = new_path + "/" + "coordinations"
        os.makedirs(new_csv_path)

        new_orijpg_path = new_path + "/" + "OriJPG"
        os.makedirs(new_orijpg_path)

        return name + "'s space has been created !"
    else:
        return name + "'s space has been created before ! "


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=5001)
    # Below for Ubuntu, upside for Windows
    app.run(host='0.0.0.0', port=5001)
