# encoding=utf-8
# Date: 2018-09-20
# Author: MJUZY


import numpy as np
from skimage import io


def Construct_Candidate(detector, sp, facerec, host_face_dirpath, host_face_jpgnames):
    """

    :param facerec:
    :param sp:
    :param detector:
    :param host_face_dirpath: dir_path + '/' + class_name + '/' + name
    :param host_face_jpgnames: [class_name + '_' + name + "_signup_1.jpg"]
    :return:
    """
    descriptors = []
    # descriptor
    # 这个列表每个元素一次储存每个人脸的特征矩阵
    # 后面计算欧式距离时会用到

    link_jpgnames = []  # 记录对应的人脸特征矩阵的所属JPG文件名

    img = ''

    for host_face_jpgname in host_face_jpgnames:

        host_face_jpgpath = host_face_dirpath + '/' + host_face_jpgname
        try:
            img = io.imread(host_face_jpgpath)

            # 人脸检测
            # 因为都是已经截好的图片，所以人脸数量必然是一
            dets = detector(img, 1)

            for k, d in enumerate(dets):
                # 关键点检测
                shape = sp(img, d)

                # 描述子提取，128D向量
                face_descriptor = facerec.compute_face_descriptor(img, shape)
                print("face_descriptor : Ok ! ")

                # 转换成numpy，array
                d_test = np.array(face_descriptor)

                # descriptor这个列表每个元素一次储存每个人脸的特征矩阵，后面计算欧式距离时会用到
                descriptors.append(d_test)

                link_jpgnames.append(host_face_jpgname)
        except:
            # <Description>: 有可能出现图片加载不了的错误
            print("Not able to Load ! ")

    return descriptors, link_jpgnames, img


def getFaceSideRate(detector, img, sp):
    # 注意，目前，side_rate 的定义，不再是，侧脸率了
    #   而是，人脸的关键点的，关键点坐标，字典，请详见下面，代码
    side_rates = [{"lip_left_xy": 0,
                   "lip_right_xy": 0}]
    """
    # Attention:
    #   scores值越大越接近正脸
    #   正常来说，只有一张脸
    #   即，只有一个side_rate
    dets, scores, idx = detector.run(img, 1)
    for i, d in enumerate(dets):
        print("Detection {}, dets{},score: {}, face_type:{}".format(i, d, scores[i], idx[i]))
        side_rates.append(scores[i])  # 越先被遍历的在数组中的下标越小
        """
    # 人脸数rects
    rects = detector(img, 0)

    # 标68个点
    if len(rects) != 0:
        # 检测，到人脸
        for i in range(len(rects)):
            landmarks = np.matrix([[p.x, p.y] for p in sp(img, rects[i]).parts()])

            # 0-26 是整个脸的，脸框     # 17-18-19-20 左眉    # 23-24-25 右眉
            # 27-30 是鼻梁
            # 37-38 是左眼框的顶部两点
            # 40-41 是左眼眶的下部两点
            # 43-44 是右眼眶上部两点
            # 46-47 是右眼框下部的两点
            # 48 是嘴唇左端，54 是嘴唇右端
            """
            point_i = 0
            
            for matrix in landmarks:
                # matrix[0, 0], matrix[0, 1]，指，x轴坐标，y轴坐标，是，传统 x-y 坐标
                #   注意，具体，x y 的关键点的意义，请调试 Try_Function_7_Get_68_Points.py

                print("point_i : ", point_i)

                point_i += 1
            """
            # 注意，请仔细看，上面的，注释
            lip_left_xy = (landmarks[48][0, 0], landmarks[48][0, 1])
            lip_right_xy = (landmarks[54][0, 0], landmarks[54][0, 1])

            side_rates[0]["lip_left_xy"] = lip_left_xy
            side_rates[0]["lip_right_xy"] = lip_right_xy

    return side_rates


def faceRecognzedProcess(detector, sp, facerec, dir_path, class_name, name, dirpath, filename, pic_file_type):
    """

        :param pic_file_type:
        :param facerec:
        :param sp:
        :param detector:
        :param dirpath: "./"
        :param filename: "kkk.jpg"

        :param dir_path: "./Accounts"
        :param class_name: "123456"
        :param name: "2171000718"
        :return:
        """
    side_rate = 0

    host_face_dirpath = dir_path + '/' + class_name + '/' + name
    host_face_jpgname = class_name + '_' + name + "_signup_1." + pic_file_type

    host_face_jpgnames = [host_face_jpgname]

    descriptors, link_jpgnames, img = Construct_Candidate(detector, sp, facerec, host_face_dirpath, host_face_jpgnames)

    Recognzed_jpgnames = [filename]

    Recognzeds_length = len(Recognzed_jpgnames)

    # 这里的描述子列表：descriptors2 储存的是签到时视频帧提取的jpg文件名，是用来得到与host 的匹配度的
    descriptors2, link_jpgnames2, img = Construct_Candidate(detector, sp, facerec, dirpath, Recognzed_jpgnames)

    tot = 0
    for des_i in descriptors2:  # <Description>: des_i是每个人脸的特征矩阵

        # 下面计算欧式距离
        dist_ = np.linalg.norm(des_i - descriptors[0])  # <Description>: des_i 是每一个视频帧jpg的人脸特征矩阵

        # 统计撞脸次数
        if dist_ < 0.384:  # <Tip>: 一般欧氏距离小于0.384就可以认为是同一张脸了，值越小说明是同一张脸的可能性越大

            side_rates = getFaceSideRate(detector, img, sp)
            if len(side_rates) > 0:
                side_rate = side_rates[0]

            tot += 1
            print("tot + 1 ! ")

    file_log = open("/var/www/demoapp/faceRecognzed_Running.txt", 'w')
    file_log.write("OK !\n")
    file_log.close()

    if tot == Recognzeds_length:
        return "Good !", side_rate
    else:
        return "Fail !", side_rate
