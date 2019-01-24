# encoding=utf-8
# Date: 2019-1-20
# Author: MJUZY


import pymysql
import re


def table_exists(c1, table_name):
    sql = "show tables;"

    c1.execute(sql)

    tables = [c1.fetchall()]

    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return True
    else:
        return False


def create_table(c1, teacher_name, course_name, op, conn):
    if not table_exists(c1, "teacher_" + teacher_name + '_' + course_name + "_" + op):

        order = "create table " + "teacher_" + teacher_name + '_' + course_name + "_" + op + " (" + \
                "teacher_name varchar(20) not null," + \
                "student_name varchar(20) not null" + \
                ");"

        c1.execute(order)
        conn.commit()

        print("Finish Creating table ! ")
    else:
        print("Table already exists ! ")

def create_arouse_table(c1, teacher_name, course_name, op, conn):
    if not table_exists(c1, "teacher_" + teacher_name + '_' + course_name + "_" + op):
        order = "create table " + "teacher_" + teacher_name + '_' + course_name + "_" + op + " (" + \
                "teacher_name varchar(20) not null," + \
                "lng_lat varchar(20) not null" + \
                ");"

        c1.execute(order)
        conn.commit()

        print("Finish create table ! ")
    else:
        order = "drop table " + "teacher_" + teacher_name + '_' + course_name + "_" + op + ";"
        c1.execute(order)
        conn.commit()

        print("Finish Delete table ! ")
        print("Now create a new table ! ")

        order = "create table " + "teacher_" + teacher_name + '_' + course_name + "_" + op + " (" + \
                "teacher_name varchar(20) not null," + \
                "lng_lat varchar(20) not null" + \
                ");"

        c1.execute(order)
        conn.commit()

        print("Finish create table ! ")


def get_lng_lat_arouse(c1, teacher_name, course_name, op, conn):
    result = True

    lng = 0
    lat = 0

    if not table_exists(c1, "teacher_" + teacher_name + '_' + course_name + "_" + op):
        result = False

        return result, lng, lat

    f1 = open("/var/www/demoapp/run.txt", 'w')
    f1.close()

    table1_name = "teacher_" + teacher_name + '_' + course_name + "_" + op

    sql = "select * from " + table1_name

    c1.execute(sql)

    contents = c1.fetchall()

    lng_lat = []

    for values in contents:
        print("lng_lat : ", values[1])
        lng_lat.append(values[1])

    temp = lng_lat[0].split("_")

    lng = float(temp[0])
    lat = float(temp[1])

    return result, lng, lat


def compare_student_names(teacher_name, course_name, op1, op2, conn):
    """

    :param teacher_name:
    :param course_name:
    :param op1: "selected"
    :param op2: "checked"
    :param conn:
    :return:
    """
    table1_name = "teacher_" + teacher_name + '_' + course_name + "_" + op1
    table2_name = "teacher_" + teacher_name + '_' + course_name + "_" + op2

    sql = "select * from " + table1_name

    c.execute(sql)

    contents = c.fetchall()

    names1 = []

    for values in contents:
        print("student name : ", values[1])
        names1.append(values[1])

    sql = "select * from " + table2_name

    c.execute(sql)

    contents = c.fetchall()

    names2 = []

    for values in contents:
        print("student name : ", values[1])
        names2.append(values[1])

    absent_names = []
    for name1 in names1:
        if name1 not in names2:
            absent_names.append(name1)

    return absent_names


def insert_arouse_table(c1, teacher_name, course_name, op, lng, lat, conn):
    order = "INSERT INTO " + "teacher_" + teacher_name + '_' + course_name + "_" + op + " VALUES (" + \
            "'" + teacher_name + "'" + ',' + \
            "'" + lng + "_" + lat + "'" + \
            ");"

    c1.execute(order)
    conn.commit()


def insert_student(c1, student_name, course_name, teacher_name, op, conn):
    create_table(c1, teacher_name, course_name, op, conn)

    table1_name = "teacher_" + teacher_name + '_' + course_name + "_" + op

    sql = "select * from " + table1_name

    c1.execute(sql)

    contents = c1.fetchall()

    for values in contents:
        print("student name : ", values[1])
        if values[1] == student_name:
            return "Exist"

    order = "INSERT INTO " + "teacher_" + teacher_name + '_' + course_name + "_" + op + " VALUES (" + \
            "'" + teacher_name + "'" + ',' + \
            "'" + student_name + "'" + \
            ");"

    c1.execute(order)
    conn.commit()

    return "Success"


def connect2Database():

    print("Now start connecting the database...")

    # connect to the database
    conn = pymysql.connect(db='CheckIn_System', user='root', passwd='270127', host='localhost', charset="utf8")

    c = conn.cursor()

    print("Finishing connecting to the database Faces ! ")

    return c, conn


if __name__ == "__main__":
    c, conn = connect2Database()

    op1 = "selected"
    op2 = "checked"
    op3 = "arouse"

    create_table(c, "xiaohaijun", "shuxue", op1, conn)

    insert_student(c, "lijingtao", "shuxue", "xiaohaijun", op1, conn)

    create_table(c, "xiaohaijun", "shuxue", op2, conn)

    insert_student(c, "lijingtao2", "shuxue", "xiaohaijun", op2, conn)

    compare_student_names("xiaohaijun", "shuxue", op1, "checked", conn)

    lng = "112"
    lat = "30"
    create_arouse_table(c, "xiaohaijun", "shuxue", op3, conn)
    insert_arouse_table(c, "xiaohaijun", "shuxue", op3, lng, lat, conn)

    get_lng_lat_arouse(c, "xiaohaijun", "shuxue", op3, conn)
