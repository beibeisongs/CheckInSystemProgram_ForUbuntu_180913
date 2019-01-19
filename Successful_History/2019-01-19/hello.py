# encoding=utf-8
# Date: 2018-09-13
# Author: MJUZY


import base64
from ExtractMaxFace import extractProcess
from FaceRecognzedProcess import faceRecognzedProcess
import datetime
import dlib
from flask import Flask
from flask import request
import json
import io
from PIL import Image
import shutil
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)


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


# Method Four: see Client\__init__.py
# app.config['UPLOAD_FOLDER'] = 'D:\\PyFlaskLearningProjects\\20180613_Test1\\static\\uploads'
# The route below is used for Ubuntu, upside for Windows
app.config['UPLOAD_FOLDER'] = '/var/www/demoapp/student_photo'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


"""Attention:

    Follows are the api-s usable -------------------------------------------------------------------------!
"""


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

        new_csv_path = new_path + "/" + "coordinations_back_up"
        os.makedirs(new_csv_path)

        new_orijpg_path = new_path + "/" + "OriJPG"
        os.makedirs(new_orijpg_path)

        return "Success"
    else:
        return "Fail"


@app.route('/sign_up_photo_upload/<class_name>/<name>', methods=['POST'])
def sign_up_photo_upload(class_name, name):
    f1 = open("/var/www/demoapp/test_result.txt", 'w')

    name = request.form.get('name', 'little apple')
    class_name = request.form.get('class_name', 'little apple')

    file_stream = request.form.get("image01")

    f1.write(str(class_name) + " " + str(name) + " " + str(file_stream))
    f1.close()

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

        pic_file_type = 'jpeg'

        extractProcess(upload_file.filename, dir, class_name, name, detector, pic_file_type)

        return "Success"
    else:
        return "Fail"


@app.route('/sign_up_photo_upload_base64/<class_name>/<name>', methods=['POST'])
def sign_up_photo_upload_base64(class_name, name):
    f1 = open("/var/www/demoapp/test_result.txt", 'w')

    file_stream = request.form.get("image01")

    f1.write(str(class_name) + " " + str(name) + " " + str(file_stream))
    f1.close()

    new_path = "/var/www/demoapp/Accounts/" + class_name + "/" + name

    base64_data_bytes = file_stream.encode("utf-8")
    base64_decode = base64.b64decode(base64_data_bytes)

    if os.path.exists(new_path) == False:
        os.makedirs(new_path)

        # Create the document storing CSV File, which used to recored customs' Travel coordinations
        new_csv_path = new_path + "/" + "coordinations"
        os.makedirs(new_csv_path)

        new_ori_jpg_path = new_path + "/" + "OriJPG"
        os.makedirs(new_ori_jpg_path)

    dirpath = '/var/www/demoapp'

    pic_file_type = 'jpeg'

    filename = name + '.' + pic_file_type

    move_to_path = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "OriJPG" + '/' + filename
    image = io.BytesIO(base64_decode)
    img = Image.open(image)
    img.save(move_to_path)

    IP = request.remote_addr

    dir = '/var/www/demoapp/Accounts'

    extractProcess(filename, dir, class_name, name, detector, pic_file_type)

    return "Success"


@app.route('/checkin_arouse/<lng>/<lat>/<course_name>/<teacher_name>', methods=['POST'])
def t_checkin_arouse(lng, lat, course_name, teacher_name):
    pass


@app.route('/checkin_lnglat_upload/<class_name>/<name>/<lng>/<lat>/<course_name>/<teacher_name>', methods=['POST'])
def u_checkin_lnglat_upload(class_name, name, lng, lat, course_name, teacher_name):
    pass


@app.route('/checkin_photo_upload1/<class_name>/<name>', methods=['POST'])
def u_checkin_upload1(class_name, name):
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

        result, side_rate = faceRecognzedProcess(detector_forcheckin, sp_forcheckin, facerec_forcheckin,
                                                 dir_path, class_name, name,
                                                 dirpath_forcheckin, upload_file.filename)

        os.remove(dirpath_forcheckin + '/' + upload_file.filename)

    if result == "Good !":
        mark_path = dir_path + '/' + class_name + '/' + name + '/' + "mark1.txt"
        file_mark = open(mark_path, 'w')
        file_mark.write(str(side_rate))
        file_mark.close()

    return result


@app.route('/checkin_photo_upload2/<class_name>/<name>', methods=['POST'])
def u_checkin_upload2(class_name, name):
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

        result, side_rate = faceRecognzedProcess(detector_forcheckin, sp_forcheckin, facerec_forcheckin,
                                                 dir_path, class_name, name,
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
            return "Fail"


def getDateStringName():
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在的时间
    construct1 = nowTime.split('-')

    year = construct1[0]
    month = construct1[1]
    day = ((construct1[2]).split(' '))[0]

    minPart = ((construct1[2]).split(' '))[1]
    construct1 = minPart.split(":")

    hour = construct1[0]
    mint = construct1[1]
    sec = construct1[2]

    return year + "_" + month + "_" + day + "_" + hour + "_" + mint + "_" + sec


@app.route('/route_data_upload/<class_name>/<name>/<lng>/<lat>/new', methods=['POST'])
def route_data_upload_new(class_name, name, lng, lat):
    dirpath = '/var/www/demoapp'
    csv_dirpath = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "coordinations"

    dateStr = getDateStringName()
    json_filepath = csv_dirpath + '/' + dateStr + ".json"

    route_data = {}
    route_data["lng"] = lng
    route_data["lat"] = lat
    a = json.dumps(route_data)
    b = str(a) + "\n"
    fh = open(json_filepath, mode='w')
    fh.write(b)
    fh.close()

    return "Success"


@app.route('/route_data_upload/<class_name>/<name>/<lng>/<lat>/middle', methods=['POST'])
def route_data_upload_middle(class_name, name, lng, lat):
    dirpath = '/var/www/demoapp'
    csv_dirpath = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "coordinations"

    for dirpath, dirnames, filenames in os.walk(csv_dirpath):
        json_filepath = csv_dirpath + '/' + filenames[0]  # Attention: There will be only one csv json file

    route_data = {}
    route_data["lng"] = lng
    route_data["lat"] = lat
    a = json.dumps(route_data)
    b = str(a) + "\n"
    fh = open(json_filepath, mode='a')
    fh.write(b)
    fh.close()

    return "Success"


@app.route('/route_data_upload/<class_name>/<name>/<lng>/<lat>/end', methods=['POST'])
def route_data_upload_end(class_name, name, lng, lat):
    dirpath = '/var/www/demoapp'
    csv_dirpath = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "coordinations"

    for dirpath, dirnames, filenames in os.walk(csv_dirpath):
        json_filepath = csv_dirpath + '/' + filenames[0]  # Attention: There will be only one csv json file

    route_data = {}
    route_data["lng"] = lng
    route_data["lat"] = lat
    a = json.dumps(route_data)
    b = str(a) + "\n"
    fh = open(json_filepath, mode='a')
    fh.write(b)
    fh.close()

    old_path = json_filepath
    new_path = '/var/www/demoapp' + "/Accounts/" + class_name + '/' + name + '/' + "coordinations_back_up"
    shutil.move(old_path, new_path)

    return "Success"


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=5001)
    # Below for Ubuntu, upside for Windows
    app.run(host='0.0.0.0', port=5001)