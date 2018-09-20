#!/usr/bin/env python
# encoding = utf-8
# Author: MUJZY
# Date: 2018-03-22


import dlib
import numpy
from skimage import io

from FaceRecognzedProcess import faceRecognzedProcess


def Construct_Candidate(host_face_dirpath, host_face_jpgnames):
    """

    :param host_face_dirpath: dir_path + '/' + class_name + '/' + name
    :param host_face_jpgnames: [class_name + '_' + name + "_signup_1.jpg"]
    :return:
    """
    descriptors = []  # descriptor
                        # 这个列表每个元素一次储存每个人脸的特征矩阵
                            # 后面计算欧式距离时会用到

    link_jpgnames = []  # 记录对应的人脸特征矩阵的所属JPG文件名

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
                d_test = numpy.array(face_descriptor)

                # descriptor这个列表每个元素一次储存每个人脸的特征矩阵，后面计算欧式距离时会用到
                descriptors.append(d_test)

                link_jpgnames.append(host_face_jpgname)
        except:
            # <Description>: 有可能出现图片加载不了的错误
            print("Not able to Load ! ")

    return descriptors, link_jpgnames


def FaceRecognition(dir_path, class_name, name, dirpath, filename):
    """

    :param dirpath: "./"
    :param filename: "kkk.jpg"

    :param dir_path: "./Accounts"
    :param class_name: "123456"
    :param name: "2171000718"
    :return:
    """

    host_face_dirpath = dir_path + '/' + class_name + '/' + name
    host_face_jpgname = class_name + '_' + name + "_signup_1.jpg"

    host_face_jpgnames = []
    host_face_jpgnames.append(host_face_jpgname)

    descriptors, link_jpgnames = Construct_Candidate(host_face_dirpath, host_face_jpgnames)

    Recognzed_jpgnames = []
    Recognzed_jpgnames.append(filename)

    Recognzeds_length = len(Recognzed_jpgnames)

    # 这里的描述子列表：descriptors2 储存的是签到时视频帧提取的jpg文件名，是用来得到与host 的匹配度的
    descriptors2, link_jpgnames2 = Construct_Candidate(dirpath, Recognzed_jpgnames)

    tot = 0
    for des_i in descriptors2:  # <Description>: des_i是每个人脸的特征矩阵

        # 下面计算欧式距离
        dist_ = numpy.linalg.norm(des_i - descriptors[0])  # <Description>: des_i 是每一个视频帧jpg的人脸特征矩阵

        # 统计撞脸次数
        if dist_ < 0.384:  # <Tip>: 一般欧氏距离小于0.384就可以认为是同一张脸了，值越小说明是同一张脸的可能性越大

            tot += 1
            print("tot + 1 ! ")

    if tot == Recognzeds_length:
        print("Result : ", "Good ! ")


def prepare_detector(predictor_path, face_rec_model_path):

    # 1、加载正脸检测器
    detector = dlib.get_frontal_face_detector()
    print("prepare_detector Ok!")
    # 2、加载人脸关键点检测器
    sp = dlib.shape_predictor(predictor_path)
    print("prepare_detector Ok!")
    # 3、加载人脸识别模型
    facerec = dlib.face_recognition_model_v1(face_rec_model_path)
    print("prepare_detector Ok!")

    return detector, sp, facerec


def prepare_path_etc():

    # 1、人脸关键点检测器
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    # 2、人脸识别模型：
    face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"

    return predictor_path, face_rec_model_path


if __name__ == "__main__":

    predictor_path, face_rec_model_path = prepare_path_etc()
    detector, sp, facerec = prepare_detector(predictor_path, face_rec_model_path)

    dirpath = "D:/PyFlaskLearningProjects/CheckInSystemProgram_ForUbuntu_180913"
    filename = "kkk.jpg"

    """Attention:
        The variables following are for the host_JPG
    """
    dir_path = "./Accounts"
    class_name = "123456"
    name = "20171000719"

    faceRecognzedProcess(detector, sp, facerec, dir_path, class_name, name, dirpath, filename)

    """
    >>>FaceRecognition(dir_path, class_name, name, dirpath, filename)
    """
