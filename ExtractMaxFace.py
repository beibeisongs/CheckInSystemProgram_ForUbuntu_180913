# encoding=utf-8
# Date: 2018-09-14
# Author: MJUZY


from PIL import Image
from skimage import io


def saveExtractedJPG(whole_jpg_path, left, top, right, bottom, new_jpg_path):
    img = Image.open(whole_jpg_path)  # Open the original JPG File

    box = (left, top, right, bottom)
    roi = img.crop(box)
    roi.save(new_jpg_path)


def startSaveExtractedJPG(jpg_dirpath, whole_jpg_path, class_name, name, d):
    """

    :param jpg_dirpath: Sample: ./Accounts/123456/20171000718/
    :param whole_jpg_path: Sample: ./Accounts/123456/20171000718/123456_20171000718.jpg
        <Attention>:
            whole_jpg_path is the original photo uploaded at first

    :param class_name: Sample: 123456
    :param name: Sample: 20171000718
    :return:
    """
    """Attention:
        All the jpg file names in the future will be constructed by four parts

        <Sample>:new_jpg_name = class_name + '_' + name + "_signup_1.jpg"

    """
    new_jpg_name = class_name + '_' + name + "_signup_1.jpg"
    new_jpg_path = jpg_dirpath + '/' + new_jpg_name

    """Read the coordination of the face 
        in the original photo
        """
    left, right, top, bottom = d.left(), d.right(), d.top(), d.bottom()
    saveExtractedJPG(whole_jpg_path, left, top, right, bottom, new_jpg_path)


def GetSelected(list):
    n = len(list)

    MAX = 0
    MAX_i = 0

    for i in range(0, n):

        if list[i] > MAX:
            MAX = list[i]
            MAX_i = i

    return MAX_i


def ExtractFaceInsideJPG_Process(detector, jpg_dirpath, whole_jpg_path, class_name, name):

    img = io.imread(whole_jpg_path)

    """
            >>>side_rate = []
            >>># scores值越大越接近正脸
            >>>dets, scores, idx = detector.run(img, 1)
            >>>for i, d in enumerate(dets):
                >>># print("Detection {}, dets{},score: {}, face_type:{}".format(i, d, scores[i], idx[i]))
                >>>side_rate.append(scores[i])  # 越先被遍历的在数组中的下标越小
            """

    """Face Detecting Process"""
    dets = detector(img, 1)

    """Record each face's Size"""
    faceSizeList = []
    for k, d in enumerate(dets):
        """
                    <Samples>:
                        left = d.left() # <Samples>: {int}451   <Description>: 人脸左边距离图片左边界的距离
                        right = d.right()   # <Samples>: {int}913   <Description>: 人脸右边距离图片左边界的距离
                        top = d.top()   # <Samples>: {int}-62   <Description>: 人脸上边距离图片上边界的距离
                        bottom = d.bottom() # <Samples>: {int}451   <Description>: 人脸下边距离图片上边界的距离
                    """
        SIZE1 = (d.right() - d.left()) * (d.bottom() - d.top())  # <Sample>: {int}
        faceSizeList.append(SIZE1)

    """Attention:

    Becase Maybe some other faces will appear in the photo
        so choose the biggest"""
    MAX_i = GetSelected(faceSizeList)

    num_of_faces = len(dets)
    if num_of_faces > 0:
        process_1_i = 0
        for k, d in enumerate(dets):
            if process_1_i == MAX_i:
                startSaveExtractedJPG(jpg_dirpath, whole_jpg_path, class_name, name, d)
            process_1_i += 1


def ExtractFaceProcess(filename, dir, class_name, name, detector):
    """

    :param detector:
    :param dir: <Sample>: '/var/www/demoapp/Accounts'
    :param class_name:
    :param name:
    :return:
    """

    """Attention:
        The jpg_path originally is the directory of the JPG File
        But then, the scripts will detect all the jpg files inside, and return a list of jpg file names
    """
    jpg_dirpath = dir + '/' + class_name + '/' + name
    whole_jpg_path = jpg_dirpath + '/' + "OriJPG" + '/' + filename

    ExtractFaceInsideJPG_Process(detector, jpg_dirpath, whole_jpg_path, class_name, name)


def extractProcess(filename, dir, class_name, name, detector):
    ExtractFaceProcess(filename, dir, class_name, name, detector)