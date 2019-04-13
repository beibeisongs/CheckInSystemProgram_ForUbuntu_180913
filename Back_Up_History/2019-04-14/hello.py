# encoding=utf-8
# Date: 2018-09-13
# Author: MJUZY


import base64
from ExtractMaxFace import extractProcess
from FaceRecognzedProcess import faceRecognzedProcess
from mysql_operation_test import *
import datetime
import dlib
from flask import Flask
from flask import request
import io
import json
import math
import os
from PIL import Image
import shutil
from werkzeug.utils import secure_filename
from urllib.request import urlopen


app = Flask(__name__)

c, conn = connect2Database()


def prepare_detector(predictor_path1, face_rec_model_path1):
    # 加载正脸检测器
    detector1 = dlib.get_frontal_face_detector()

    # 加载人脸关键点检测器
    sp1 = dlib.shape_predictor(predictor_path1)

    # 加载人脸识别模型
    facerec1 = dlib.face_recognition_model_v1(face_rec_model_path1)

    return detector1, sp1, facerec1


def prepare_path_etc():
    # 人脸关键点检测器
    predictor_path1 = "/var/www/demoapp/shape_predictor_68_face_landmarks.dat"
    # 人脸识别模型：
    face_rec_model_path1 = "/var/www/demoapp/dlib_face_recognition_resnet_model_v1.dat"

    return predictor_path1, face_rec_model_path1


predictor_path, face_rec_model_path = prepare_path_etc()
detector, sp, facerec = prepare_detector(predictor_path, face_rec_model_path)


# Method Four: see Client\__init__.py
# app.config['UPLOAD_FOLDER'] = 'D:\\PyFlaskLearningProjects\\20180613_Test1\\static\\uploads'
# The route below is used for Ubuntu, upside for Windows
app.config['UPLOAD_FOLDER'] = '/var/www/demoapp/student_photo'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


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

    # Get the client's IP
    # IP = request.remote_addr

    class_name = request.form.get("class_name")
    name = request.form.get("name")

    new_path = "/var/www/demoapp/Accounts/" + class_name + "/" + name
    if not os.path.exists(new_path):
        os.makedirs(new_path)

        # Create the document storing CSV File, which used to recored customs' Travel coordinations
        new_csv_path = new_path + "/" + "coordinations"
        os.makedirs(new_csv_path)

        new_csv_path = new_path + "/" + "coordinations_back_up"
        os.makedirs(new_csv_path)

        new_ori_jpg_path = new_path + "/" + "OriJPG"
        os.makedirs(new_ori_jpg_path)

        return "Success"
    else:
        return "Fail"


@app.route('/login/<class_name>/<name>', methods=['POST'])
def u_login(class_name, name):
    if os.path.exists("/var/www/demoapp/Accounts/" + class_name + '/' + name):
        return "Yes"
    else:
        return "No"


@app.route('/sign_up_photo_upload/<class_name>/<name>', methods=['POST'])
def sign_up_photo_upload(class_name, name):

    new_path = "/var/www/demoapp/Accounts/" + class_name + "/" + name

    if not os.path.exists(new_path):
        os.makedirs(new_path)

        # Create the document storing CSV File, which used to record customs' Travel coordinations
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

        # Get the Client's IP
        # IP = request.remote_addr

        dir_path = '/var/www/demoapp/Accounts'

        pic_file_type = 'jpeg'

        extractProcess(upload_file.filename, dir_path, class_name, name, detector, pic_file_type)

        return "Success"
    else:
        return "Fail"


@app.route('/sign_up_photo_upload_base64/<class_name>/<name>', methods=['POST'])
def sign_up_photo_upload_base64(class_name, name):

    file_stream = request.form.get("image01")

    new_path = "/var/www/demoapp/Accounts/" + class_name + "/" + name

    base64_data_bytes = file_stream.encode("utf-8")
    base64_decode = base64.b64decode(base64_data_bytes)

    if not os.path.exists(new_path):
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

    # Get the Client's IP
    # IP = request.remote_addr

    dir_path = '/var/www/demoapp/Accounts'

    extractProcess(filename, dir_path, class_name, name, detector, pic_file_type)

    return "Success"


@app.route('/select_course/<class_name>/<name>', methods=['POST'])
def select_course(class_name, name):
    print(class_name)

    course_name = request.form.get("course_name")

    teacher_name = request.form.get("teacher_name")

    operation1 = "selected"

    response = insert_student(c, name, course_name, teacher_name, operation1, conn)

    return response


@app.route('/checkin_arouse/<lng1>/<lat1>/<course_name>/<teacher_name>', methods=['POST'])
def t_checkin_arouse(lng1, lat1, course_name, teacher_name):
    operation3 = "arouse"
    create_arouse_table(c, teacher_name, course_name, operation3, conn)
    insert_arouse_table(c, teacher_name, course_name, operation3, lng1, lat1, conn)

    return "Success !"


@app.route('/checkin_photo_upload1/<class_name>/<name>/<lng1>/<lat1>', methods=['POST'])
def u_checkin_upload1(class_name, name, lng1, lat1):
    """Attention:

        Now stipulate that Only Two Photos will be uploaded
            And This api used for the first photo uploaded

    :return:

    """
    course_name = request.form.get("course_name")

    teacher_name = request.form.get("teacher_name")

    operation3 = "arouse"
    result_get_lnglat, t_lng, t_lat = get_lng_lat_arouse(c, teacher_name, course_name, operation3, conn)

    if not result_get_lnglat:
        return "No Arousing Yet ! "

    file_stream = request.form.get("image01")

    base64_data_bytes = file_stream.encode("utf-8")
    base64_decode = base64.b64decode(base64_data_bytes)

    dirpath = '/var/www/demoapp'

    pic_file_type = 'jpeg'

    filename = name + "upload1" + '.' + pic_file_type

    move_to_path = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "OriJPG" + '/' + filename
    image = io.BytesIO(base64_decode)
    img = Image.open(image)
    img.save(move_to_path)

    # Get the client's IP
    # IP = request.remote_addr

    detector_forcheckin = detector

    sp_forcheckin = sp

    facerec_forcheckin = facerec

    dir_path = '/var/www/demoapp/Accounts'

    dirpath_forcheckin = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "OriJPG"

    result, side_rate = faceRecognzedProcess(detector_forcheckin, sp_forcheckin, facerec_forcheckin,
                                             dir_path, class_name, name,
                                             dirpath_forcheckin, filename, pic_file_type)

    os.remove(dirpath_forcheckin + '/' + filename)

    if result == "Good !":
        mark_path = dir_path + '/' + class_name + '/' + name + '/' + "mark1.txt"
        file_mark = open(mark_path, 'w')

        # 注意，1，代表，嘴唇判别，模式
        file_mark.write(str("1") + "-" + str(lng1) + "-" + str(lat1) + "-" +
                        str(side_rate["lip_left_xy"][0]) + "-" +
                        str(side_rate["lip_left_xy"][1]) + "-" +
                        str(side_rate["lip_right_xy"][0]) + "-" +
                        str(side_rate["lip_right_xy"][1]))

        file_mark.close()

        # 注意，之后，这里会，设置，随机函数，同时，check_face_motion 的，数字类型，会更加丰富
        #   “1”，指，微笑
        check_face_motion = "1"

        return check_face_motion
    else:
        return "Fail"


@app.route('/checkin_photo_upload2_alive_detect/<class_name>/<name>', methods=['POST'])
def u_checkin_upload2_alive_detect(class_name, name):
    """Attention:

        Now stipulate that Only Two Photos will be uploaded
            And This api used for the first photo uploaded

    :return:

    """
    course_name = request.form.get("course_name")

    teacher_name = request.form.get("teacher_name")

    file_stream = request.form.get("image01")

    base64_data_bytes = file_stream.encode("utf-8")
    base64_decode = base64.b64decode(base64_data_bytes)

    dirpath = '/var/www/demoapp'

    pic_file_type = 'jpeg'

    filename = name + "upload2" + '.' + pic_file_type

    move_to_path = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "OriJPG" + '/' + filename
    image = io.BytesIO(base64_decode)
    img = Image.open(image)
    img.save(move_to_path)

    detector_forcheckin = detector

    sp_forcheckin = sp

    facerec_forcheckin = facerec

    dir_path = '/var/www/demoapp/Accounts'

    dirpath_forcheckin = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "OriJPG"

    result, side_rate = faceRecognzedProcess(detector_forcheckin, sp_forcheckin, facerec_forcheckin,
                                             dir_path, class_name, name,
                                             dirpath_forcheckin, filename, pic_file_type)

    os.remove(dirpath_forcheckin + '/' + filename)

    face_check_left_x_now = side_rate["lip_left_xy"][0]
    # face_check_left_y_now = side_rate["lip_left_xy"][1]
    face_check_right_x_now = side_rate["lip_right_xy"][0]
    # face_check_right_y_now = side_rate["lip_right_xy"][1]

    if result == "Good !":
        mark_path = dir_path + '/' + class_name + '/' + name + '/' + "mark1.txt"
        if os.path.exists(mark_path):
            file_mark = open(mark_path, 'r')

            side_rate_1 = file_mark.read()
            side_rate_1 = side_rate_1.split("-")

            s_lng = float(side_rate_1[1])
            s_lat = float(side_rate_1[2])

            # 这个码，代表着，选用某种模式，比如，1，代表，微笑，识别
            face_check_mode = int(side_rate_1[0])

            # 注意，联，FaceRecognzedProcess.py line 85-107
            face_check_left_x_history = int(side_rate_1[3])
            # face_check_left_y_history = int(side_rate_1[4])
            face_check_right_x_history = int(side_rate_1[5])
            # face_check_right_y_history = int(side_rate_1[6])

            judge_result = False
            if face_check_mode == 1:
                key_points_distance_history = face_check_right_x_history - face_check_left_x_history
                key_points_distance_now = face_check_right_x_now - face_check_left_x_now

                if key_points_distance_now > key_points_distance_history:
                    judge_result = True

            file_mark.close()

            os.remove(mark_path)

            operation3 = "arouse"
            result_get_lnglat, t_lng, t_lat = get_lng_lat_arouse(c, teacher_name, course_name, operation3, conn)

            distance = math.sqrt((t_lng - s_lng) * (t_lng - s_lng) + (t_lat - s_lat) * (t_lat - s_lat))

            if abs(float(side_rate_1[0]) - float(side_rate)) == 0:
                result = "Same_Side_Rate_"
                return result + str(distance)

            if not judge_result:
                return "Face_Fail_" + str(distance)

            operation2 = "checked"
            insert_student(c, name, course_name, teacher_name, operation2, conn)

            return "Good_" + str(distance)
        else:
            return "Face_Fail"


@app.route('/checkin_photo_upload2/<class_name>/<name>', methods=['POST'])
def u_checkin_upload2(class_name, name):
    """Attention:

        Now stipulate that Only Two Photos will be uploaded
            And This api used for the first photo uploaded

    :return:

    """
    course_name = request.form.get("course_name")

    teacher_name = request.form.get("teacher_name")

    file_stream = request.form.get("image01")

    base64_data_bytes = file_stream.encode("utf-8")
    base64_decode = base64.b64decode(base64_data_bytes)

    dirpath = '/var/www/demoapp'

    pic_file_type = 'jpeg'

    filename = name + "upload2" + '.' + pic_file_type

    move_to_path = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "OriJPG" + '/' + filename
    image = io.BytesIO(base64_decode)
    img = Image.open(image)
    img.save(move_to_path)

    detector_forcheckin = detector

    sp_forcheckin = sp

    facerec_forcheckin = facerec

    dir_path = '/var/www/demoapp/Accounts'

    dirpath_forcheckin = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "OriJPG"

    result, side_rate = faceRecognzedProcess(detector_forcheckin, sp_forcheckin, facerec_forcheckin,
                                             dir_path, class_name, name,
                                             dirpath_forcheckin, filename, pic_file_type)

    os.remove(dirpath_forcheckin + '/' + filename)

    if result == "Good !":
        mark_path = dir_path + '/' + class_name + '/' + name + '/' + "mark1.txt"
        if os.path.exists(mark_path):
            file_mark = open(mark_path, 'r')

            side_rate_1 = file_mark.read()
            side_rate_1 = side_rate_1.split("-")

            s_lng = float(side_rate_1[1])
            s_lat = float(side_rate_1[2])

            file_mark.close()

            os.remove(mark_path)

            operation3 = "arouse"
            result_get_lnglat, t_lng, t_lat = get_lng_lat_arouse(c, teacher_name, course_name, operation3, conn)

            distance = math.sqrt((t_lng - s_lng) * (t_lng - s_lng) + (t_lat - s_lat) * (t_lat - s_lat))

            if abs(float(side_rate_1[0]) - float(side_rate)) == 0:
                result = "Same Side Rate !!!"
                return result + str(distance)

            operation2 = "checked"
            insert_student(c, name, course_name, teacher_name, operation2, conn)

            return result + str(distance)
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


url_drive = r"https://restapi.amap.com/v3/direction/driving?output=json"
strategy_type = r"&strategy=0"
ak = r"&key=af1a4cdccb910ab935506791e930ca4a"


def call_road_guide_api(lng1, lat1, destination_lng, destination_lat):
    origin = str(lng1) + ',' + str(lat1)

    destination = str(destination_lng) + ',' + str(destination_lat)

    json_to_front = {"status": "fail"}
    try:
        ori = r"&origin=" + origin
        des = r"&destination=" + destination
        get_url = url_drive + ori + des + strategy_type + ak

        res_drive = urlopen(get_url)
        cet_drive = res_drive.read()
        cet_drive = str(cet_drive, encoding='utf-8')

        result_drive = json.loads(cet_drive)
        status = result_drive['status']
        if status == 0:
            return "failed"

        road_info = result_drive['route']

        taxi_cost = road_info['taxi_cost']

        paths = road_info['paths']
        for j in range(len(paths)):
            distance = paths[j]['distance']
            duration = paths[j]['duration']

            hour = int(int(duration) / 3600)
            mintue = int(int(duration) / 60) - (hour * 60)
            second = int(duration) - (hour * 3600) - (mintue * 60)

            strategy = paths[j]['strategy']

            steps = paths[j]['steps']

            polyline = []
            for k in range(len(steps)):
                polyline.append(steps[k]['polyline'])

            """
            path_info = "采用策略：" + strategy + "\n" + "路程距离：" + str(distance) + "m" \
                        + " 用时：" + str(hour) + ":" + str(mintue) + ":" + str(second)
            """

            points = []
            for m in range(len(polyline)):
                point = str(polyline[m]).split(';')
                for each in point:
                    lng_lat = each.split(',')

                    points.append(float(lng_lat[0]))
                    points.append(float(lng_lat[1]))

            json_to_front = {"strategy": strategy, "distance": float(distance),
                             "taxi_cost": taxi_cost, "plan_points": points,
                             "lng": lng1, "lat": lat1,
                             "destination_lng": destination_lng, "destination_lat": destination_lat,
                             "time_cost": str(hour) + ":" + str(mintue) + ":" + str(second),
                             "status": "success",
                             "distance_change": 0
                             }
            return json_to_front
    except:
        pass

    return json_to_front


@app.route('/route_data_upload/<class_name>/<name>/<lng1>/<lat1>/new', methods=['POST'])
def route_data_upload_new(class_name, name, lng1, lat1):
    """
        Attention, please
            route_data_upload_new, is activated
                just before the student decide to call the taxi driver

            So, what route_data_upload gets
                is the coordination of the starting point

                and the coordination of the destination
    """
    destination_lng = request.form.get("destination_lng")

    destination_lat = request.form.get("destination_lat")

    dirpath = '/var/www/demoapp'
    json_dirpath = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "coordinations"

    dateStr = getDateStringName()
    json_filepath = json_dirpath + '/' + dateStr + ".json"

    json_to_front = call_road_guide_api(lng1, lat1, destination_lng, destination_lat)

    json_temp = json.dumps(json_to_front, ensure_ascii=False)

    b = str(json_temp) + "\n"

    fh = open(json_filepath, mode='w')
    fh.write(b)
    fh.close()

    return json_temp


@app.route('/route_data_upload/<class_name>/<name>/<lng1>/<lat1>/middle', methods=['POST'])
def route_data_upload_middle(class_name, name, lng1, lat1):
    dirpath = '/var/www/demoapp'
    json_dirpath = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "coordinations"

    for dirpath, dirnames, filenames in os.walk(json_dirpath):
        json_filepath = json_dirpath + '/' + filenames[0]  # Attention: There will be only one csv json file

        destination_lat = destination_lng = distance_before = ''

        with open(json_filepath, mode='r', encoding="utf-8") as f_read:
            for line in f_read.readlines():
                rline = json.loads(line)

                distance_before = rline["distance"]

                destination_lng = rline["destination_lng"]
                destination_lat = rline["destination_lat"]

        json_to_front = call_road_guide_api(lng1, lat1, destination_lng, destination_lat)

        distance_now = json_to_front["distance"]

        json_to_front["distance_change"] = distance_now - distance_before

        b = str(json.dumps(json_to_front)) + "\n"

        fh = open(json_filepath, mode='a+', encoding="utf-8")
        fh.write(b)
        fh.close()

        return json_to_front


@app.route('/route_data_upload/<class_name>/<name>/<lng1>/<lat1>/end', methods=['POST'])
def route_data_upload_end(class_name, name, lng1, lat1):
    dirpath = '/var/www/demoapp'
    json_dirpath = dirpath + "/Accounts/" + class_name + '/' + name + '/' + "coordinations"

    for dirpath, dirnames, filenames in os.walk(json_dirpath):
        json_filepath = json_dirpath + '/' + filenames[0]  # Attention: There will be only one csv json file

        destination_lat = destination_lng = distance_before = ''

        with open(json_filepath, mode='r', encoding="utf-8") as f_read:
            for line in f_read.readlines():
                rline = json.loads(line)

                distance_before = rline["distance"]

                destination_lng = rline["destination_lng"]
                destination_lat = rline["destination_lat"]

        json_to_front = call_road_guide_api(lng1, lat1, destination_lng, destination_lat)

        distance_now = json_to_front["distance"]

        json_to_front["distance_change"] = distance_now - distance_before

        b = str(json.dumps(json_to_front)) + "\n"

        fh = open(json_filepath, mode='a+', encoding="utf-8")
        fh.write(b)
        fh.close()

        old_path = json_filepath
        new_path = '/var/www/demoapp' + "/Accounts/" + class_name + '/' + name + '/' + "coordinations_back_up"
        shutil.move(old_path, new_path)

        return json_to_front


@app.route('/checkin_find_absent/<course_name>/<teacher_name>', methods=['POST'])
def checkin_find_absent(course_name, teacher_name):
    absent_names = compare_student_names(teacher_name, course_name, "selected", "checked", c)

    absent_names_string = ''
    for name in absent_names:
        absent_names_string += name + ' '

    return absent_names_string


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=5001)
    # Below for Ubuntu, upside for Windows
    app.run(host='0.0.0.0', port=5001)
