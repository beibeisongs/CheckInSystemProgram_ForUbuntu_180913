# encoding=utf-8
# Date: 2018-09-13
# Author: MJUZY


from ExtractMaxFace import extractProcess
from FaceRecognzedProcess import faceRecognzedProcess
import dlib
from flask import Flask, url_for
from flask import request
import json
import shutil
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

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

"""Attention:
    This is just the sample of the usage of the cache

>>>from werkzeug.contrib.cache import SimpleCache

>>>cache = SimpleCache()
>>>cache.set("detector", detector)
>>>cache.set("sp", sp)

>>>cache.set("facerec", facerec)
>>>cache.get("detector")
>>>...

"""


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
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/sign_up_photo_upload', methods=['POST'])
def upload():
    name = request.form.get('name', 'little apple')
    class_name = request.form.get('class_name', 'little apple')

    new_path = "/var/www/demoapp/Accounts/" + class_name + "/" + name

    if os.path.exists(new_path) == False:
        os.makedirs(new_path)

        # Create the document storing CSV File, which used to recored customs' Travel coordinations
        new_csv_path = new_path + "/" + "coordinations"

        os.makedirs(new_csv_path)

        new_orijpg_path = new_path + "/" + "OriJPG"

        os.makedirs(new_orijpg_path)

    dirpath = '/var/www/demoapp'

    upload_file = request.files['image01']

    if upload_file and allowed_file(upload_file.filename):

        filename = secure_filename(upload_file.filename)

        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))

        sign_up_photo_path = dirpath + "/student_photo/" + str(upload_file.filename)

        move_to_path = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "OriJPG"

        shutil.move(sign_up_photo_path, move_to_path)

        """Description: the orders following are used to check if the scripts have been correctly executed

        >>>log_file = open('/var/www/demoapp/log.txt', mode='a')
        >>>log_file.write("---shutil.move Ok !---")

        """

        IP = request.remote_addr

        dir = '/var/www/demoapp/Accounts'

        extractProcess(upload_file.filename, dir, class_name, name, detector)

        return 'hello, ' + name + ' class_name: ' + class_name + 'IP : ' + IP + ' success'

    else:
        return 'hello, ' + request.form.get('name', 'little apple') + ' failed'


@app.route('/checkin_photo_upload1', methods=['POST'])
def checkin_upload1():
    """Attention:

        Now stipulate that Only Two Photos will be uploaded
            And This api used for the first photo uploaded

    :return:

    """
    side_rate = 0

    result = "This is the Original Value of the result !"

    detector_forcheckin = detector

    sp_forcheckin = sp

    facerec_forcheckin = facerec

    dir_path = '/var/www/demoapp/Accounts'

    dirpath_forcheckin = "/var/www/demoapp/student_photo"

    upload_file = request.files['image01']

    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)

        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))

        name = request.form.get('name', 'little apple')

        class_name = request.form.get('class_name', 'little apple')

        result, side_rate = faceRecognzedProcess(detector_forcheckin, sp_forcheckin, facerec_forcheckin,
                                      dir_path, class_name,name,
                                      dirpath_forcheckin, upload_file.filename)

        os.remove(dirpath_forcheckin + '/' + upload_file.filename)

    if result == "Good !":
        mark_path = dir_path + '/' + class_name + '/' + name + '/' + "mark1.txt"
        file_mark = open(mark_path, 'w')
        file_mark.write(str(side_rate))
        file_mark.close()

    return result


@app.route('/checkin_photo_upload2', methods=['POST'])
def checkin_upload2():
    """Attention:

        Now stipulate that Only Two Photos will be uploaded
            And This api used for the first photo uploaded

    :return:

    """
    side_rate = 0

    result = "This is the Original Value of the result !"

    detector_forcheckin = detector

    sp_forcheckin = sp

    facerec_forcheckin = facerec

    dir_path = '/var/www/demoapp/Accounts'

    dirpath_forcheckin = "/var/www/demoapp/student_photo"

    upload_file = request.files['image01']

    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)

        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))

        name = request.form.get('name', 'little apple')

        class_name = request.form.get('class_name', 'little apple')

        result, side_rate = faceRecognzedProcess(detector_forcheckin, sp_forcheckin, facerec_forcheckin,
                                      dir_path, class_name,name,
                                      dirpath_forcheckin, upload_file.filename)

        os.remove(dirpath_forcheckin + '/' + upload_file.filename)

    if result == "Good !":
        mark_path = dir_path + '/' + class_name + '/' + name + '/' + "mark1.txt"
        if os.path.exists(mark_path) == True:
            file_mark = open(mark_path, 'r')

            side_rate_1 = file_mark.read()
            if abs(float(side_rate_1) - float(side_rate)) == 0:
                result = "Same Side Rate !!!"

            file_mark.close()

            os.remove(mark_path)

            return result
        else:
            return "Fail !"


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


@app.route('/post_function_test1', methods=['POST'])
def post_function_test():
    name = request.form.get('name', 'little apple')
    class_name = request.form.get('class_name', 'little apple')

    IP = request.remote_addr

    file = open("/var/www/demoapp/post_function_test.txt", 'w')
    file.close()

    return 'hello, ' + name + ' class_name: ' + class_name + ' IP : ' + IP + ' success'


@app.route('/student_create_space', methods=['POST'])
def student_create_space():

    # name = request.form.get('name', 'little apple')
    # class_name = request.form.get('class_name', 'little apple')
    # name = request.form['name']
    # class_name = request.form['class_name']

    IP = request.remote_addr

    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))

    name = json_data.get("name")
    class_name = json_data.get("class_name")

    new_path = "/var/www/demoapp/Accounts/" + class_name + "/" + name
    if os.path.exists(new_path) == False:
        os.makedirs(new_path)

        # Create the document storing CSV File, which used to recored customs' Travel coordinations
        new_csv_path = new_path + "/" + "coordinations"
        os.makedirs(new_csv_path)

        new_orijpg_path = new_path + "/" + "OriJPG"
        os.makedirs(new_orijpg_path)

        return 'hello, ' + name + ' class_name: ' + class_name + ' IP : ' + IP + ' success'
    else:
        return name + "'s space has been created before ! "


@app.route('/sign_up_photo_upload/<class_name>/<name>', methods=['POST'])
def sign_up_photo_upload(class_name, name):

    new_path = "/var/www/demoapp/Accounts/" + class_name + "/" + name

    if os.path.exists(new_path) == False:
        os.makedirs(new_path)

        # Create the document storing CSV File, which used to recored customs' Travel coordinations
        new_csv_path = new_path + "/" + "coordinations"

        os.makedirs(new_csv_path)

        new_orijpg_path = new_path + "/" + "OriJPG"

        os.makedirs(new_orijpg_path)

    dirpath = '/var/www/demoapp'

    upload_file = request.files['image01']

    if upload_file and allowed_file(upload_file.filename):

        filename = secure_filename(upload_file.filename)

        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))

        sign_up_photo_path = dirpath + "/student_photo/" + str(upload_file.filename)

        move_to_path = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "OriJPG"

        shutil.move(sign_up_photo_path, move_to_path)

        """Description: the orders following are used to check if the scripts have been correctly executed

        >>>log_file = open('/var/www/demoapp/log.txt', mode='a')
        >>>log_file.write("---shutil.move Ok !---")

        """

        IP = request.remote_addr

        dir = '/var/www/demoapp/Accounts'

        extractProcess(upload_file.filename, dir, class_name, name, detector)

        return 'hello, ' + name + ' class_name: ' + class_name + 'IP : ' + IP + ' success'

    else:
        return 'hello, ' + request.form.get('name', 'little apple') + ' failed'


if __name__ == "__main__":

    # app.run(host='127.0.0.1', port=5001)
    # Below for Ubuntu, upside for Windows
    app.run(host='0.0.0.0', port=5001)
