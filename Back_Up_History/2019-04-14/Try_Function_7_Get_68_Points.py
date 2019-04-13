# encoding=utf-8
# Date: 2019-4-9
# Author: MJUZY


import dlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skimage import io


def prepare_detector(predictor_path1, face_rec_model_path1):
    # 加载，正脸检测器
    detector1 = dlib.get_frontal_face_detector()
    print("日志：加载，正脸检测器，完成")

    # 加载，人脸关键点检测器
    sp1 = dlib.shape_predictor(predictor_path1)
    print("日志：加载，人脸关键点检测器，完成")

    # 加载，人脸识别模型
    facerec1 = dlib.face_recognition_model_v1(face_rec_model_path1)
    print("日志：加载，人脸识别模型，完成")

    return detector1, sp1, facerec1


def prepare_path_etc():
    # 人脸关键点检测器
    predictor_path1 = "./shape_predictor_68_face_landmarks.dat"
    # 人脸识别模型：
    face_rec_model_path1 = "./dlib_face_recognition_resnet_model_v1.dat"

    return predictor_path1, face_rec_model_path1


def walk_file():
    img = io.imread(dir_path + file_name + data_type)

    # 人脸数rects
    rects = detector(img, 0)

    img_pil = Image.open(dir_path + file_name + data_type)

    plt.imshow(img_pil)

    # 标68个点
    if len(rects) != 0:
        # 检测，到人脸
        for i in range(len(rects)):
            landmarks = np.matrix([[p.x, p.y] for p in sp(img, rects[i]).parts()])
            print(landmarks.shape)

            colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

            markers = ['o', 's', 'D', 'v', '^', 'p', '*']

            plt.figure()
            # 0-26 是整个脸的，脸框     # 17-18-19-20 左眉    # 23-24-25 右眉
            # 27-30 是鼻梁
            # 37-38 是左眼框的顶部两点
            # 40-41 是左眼眶的下部两点
            # 43-44 是右眼眶上部两点
            # 46-47 是右眼框下部的两点
            # 48 是嘴唇左端，54 是嘴唇右端
            # 注意，下面是，坐标提取的，示例
            # print(landmarks[17][0, 0], landmarks[17][0, 1])
            point_i = 0
            for matrix in landmarks:

                plt.plot(matrix[0, 0], matrix[0, 1], color=colors[1], markersize=3, marker=markers[1], alpha=0.5)
                print("point_i : ", point_i, matrix[0, 0], matrix[0, 1])

                point_i += 1

            print(input())

if __name__ == "__main__":
    data_type = ".jpeg"

    file_name = "kkk"

    dir_path = "./"

    predictor_path, face_rec_model_path = prepare_path_etc()
    detector, sp, facerec = prepare_detector(predictor_path, face_rec_model_path)

    walk_file()
