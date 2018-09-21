# encoding=utf-8
# Date: 2018-09-20


import json
from urllib.request import urlopen


# 百度地图提供的服务网址
url_drive = r"http://api.map.baidu.com/routematrix/v2/driving?output=json"  # 驾车
url_ride = r'http://api.map.baidu.com/routematrix/v2/riding?output=json'  # 骑行
url_walk = r'http://api.map.baidu.com/routematrix/v2/walking?output=json'  # 步行
url_bus = r'http://api.map.baidu.com/direction/v2/transit?output=json'  # bus

cod = r"&coord_type=wgs84"

# 声明坐标格式，bd09ll（百度经纬度坐标）；bd09mc（百度摩卡托坐标）；gcj02（国测局加密坐标）；wgs84（gps设备获取的坐标）
tac_type = r"&tactics=10"  # 10不走高速 ；11常规路线；12距离较短；13距离较短（不考虑路况） 只对驾车有效

ak = r"&ak=xop0xOYgFxbts1hZhT8YAS2o4BoKfDZp"  # ak为从百度地图网站申请的秘钥

lat_origin = [23.1673720000, 23.1305729094, 23.1252054986, 23.2066407279, 23.2691039040, 23.2754905346]

lng_origin = [113.3984980000, 113.2570266724, 113.1761741638, 113.2080173492, 113.3985614777, 113.8157844543]

lat_destination = [22.9886470000, 23.1394128825, 23.1979629753, 23.3201095519, 23.3365816945, 23.2227325231]

lng_destinaton = [113.2691620000, 113.3453464508, 113.2804584503, 113.6949348450, 113.3973598480, 113.4921169281]

origin = []

for i in range(len(lat_origin)):
    lat1 = lat_origin[i]
    lng1 = lng_origin[i]

    origin1 = str(lat1) + ',' + str(lng1)

    origin.append(origin1)

print(origin)

destination = []

for i in range(len(lat_destination)):
    lat2 = lat_destination[i]
    lng2 = lng_destinaton[i]

    destination2 = str(lat2) + ',' + str(lng2)

    destination.append(destination2)

print(destination)

'''
    起点坐标

origin = {'23.1673720000,113.3984980000','23.1305729094,113.2570266724',

            '23.1252054986,113.1761741638','23.2066407279,113.2080173492',

            '23.2691039040,113.3985614777','23.2754905346,113.8157844543'}

    终点坐标

destination ={ '22.9886470000,113.2691620000','23.1394128825,113.3453464508',

                '23.1979629753,113.2804584503' ,'23.3201095519,113.6949348450',

                '23.3365816945,113.3973598480','23.2227325231,113.4921169281'}'''

colnames = '起点 终点 驾车距离(公里) 驾车距离(米) 驾车时长(小时) 驾车时长(秒) 驾车油费(元) 的士车费(元) 骑行距离(公里) 骑行距离(米) 骑行时长(小时) 骑行时长(秒) 步行距离(公里) 步行距离(米) 步行时长(小时) 步行时长(秒) 乘车距离(公里) 乘车距离(米) 乘车时长(小时) 乘车时长(秒) 乘车费用(元)'

with open("/stimecol.txt", 'a', encoding='utf-8') as f:
    f.write(colnames)  # 把变量名先写入文件
    f.write('\n')
    f.close()

try:

    for ori1 in origin:
        for des1 in destination:

            ori = r"&origins=" + ori1
            des = r"&destinations=" + des1

            tac_type = r'&tactics=10'  # 驾车路径选择

            aurl_drive = url_drive + ori + des + cod + tac_type + ak

            aurl_ride = url_ride + ori + des + cod + tac_type + ak

            aurl_walk = url_walk + ori + des + cod + tac_type + ak

            print("aurl_drive : ", aurl_drive)

            # 以下是自驾车

            res_drive = urlopen(aurl_drive)

            cet_drive = res_drive.read()

            result_drive = json.loads(cet_drive)
            print("result_drive : ", result_drive)

            status = result_drive['status']
            print(status)

            if status == 1 or status == 2:

                continue

            else:

                print('gooddrive')

            km_drive = result_drive['result'][0]['distance']['text']

            m_drive = result_drive['result'][0]['distance']['value']

            time_drive = result_drive['result'][0]['duration']['text']

            timesec_drive = result_drive['result'][0]['duration']['value']

            # 按93#汽油，6.8元每升。这样，一公里的油耗费用：7/100*6.8=0.476元

            cost_drive = round(m_drive * 0.476 / 1000, 2)  # 自驾车油费

            if m_drive < 2500:  # 同样距离的士费用

                cost_taxi = 10.00  # 2.5km内10元

            elif m_drive < 35000 and m_drive > 2500:

                cost_taxi = round(10 + (m_drive - 2500) * 2.5 / 1000, 2)  # 超过2.5km部分2.5元/km

            elif m_drive > 35000:

                cost_taxi = round(10 + (35000 - 2500) * 2.5 / 1000 + (m_drive - 35000) * 3.9 / 1000,
                                  2)  # 超过35km部分3.9元/km

            diss_drive = km_drive + ' ' + str(m_drive) + ' ' + time_drive + ' ' + str(timesec_drive) + ' ' + str(
                                    cost_drive) + ' ' + str(cost_taxi)
            print("diss_drive : ", diss_drive)

            # 以下是骑行

            res_ride = urlopen(aurl_ride)

            cet_ride = res_ride.read()

            result_ride = json.loads(cet_ride)

            print("result_ride : ", result_ride)

            status = result_ride['status']

            print("status : ", status)

            if status == 1 or status == 2:

                continue

            else:

                print('goodride')

            km_ride = result_ride['result'][0]['distance']['text']

            m_ride = result_ride['result'][0]['distance']['value']

            time_ride = result_ride['result'][0]['duration']['text']

            timesec_ride = result_ride['result'][0]['duration']['value']

            diss_ride = km_ride + ' ' + str(m_ride) + ' ' + time_ride + ' ' + str(timesec_ride)

            print("diss_ride : ", diss_ride)

            # 以下是步行

            res_walk = urlopen(aurl_walk)

            cet_walk = res_walk.read()

            result_walk = json.loads(cet_walk)

            print("result_walk : ", result_walk)

            status = result_walk['status']

            print("status : ", status)

            if status == 1 or status == 2:

                continue

            else:

                print('goodwalk')

            km_walk = result_walk['result'][0]['distance']['text']

            m_walk = result_walk['result'][0]['distance']['value']

            time_walk = result_walk['result'][0]['duration']['text']

            timesec_walk = result_walk['result'][0]['duration']['value']

            diss_walk = km_walk + ' ' + str(m_walk) + ' ' + time_walk + ' ' + str(timesec_walk)

            print(diss_walk)

            # 以下是乘车（推荐路线）

            tac_bus = r'&tactics_incity=0'

            # 市内公交换乘策略 可选，默认为0      0推荐；1少换乘；2少步行；3不坐地铁；4时间短；5地铁优先

            city_bus = r'&tactics_intercity=0'

            # 跨城公交换乘策略  可选，默认为0    0时间短；1出发早；2价格低；

            city_type = r'&trans_type_intercity=0'

            # 跨城交通方式策略  可选，默认为0  0火车优先；1飞机优先；2大巴优先；

            ori2 = r"&origin=" + ori1

            des2 = r"&destination=" + des1

            aurl_bus = url_bus + ori2 + des2 + cod + tac_bus + city_bus + city_type + ak

            print("aurl_bus", aurl_bus)

            res_bus = urlopen(aurl_bus)

            cet_bus = res_bus.read()

            result_bus = json.loads(cet_bus)

            print("result_bus", result_bus)

            status = result_bus['status']

            print("status : ", status)

            if status == 1 or status == 2:

                continue

            else:

                print('goodbus')

            # bus代表乘车

            m_bus = result_bus['result']['routes'][0]['distance']  # 乘车路线距离总长（m）

            km_bus = round(m_bus / 1000, 2)  # 公里

            time_bus = result_bus['result']['routes'][0]['duration']  # 乘车时间（秒）

            timehour_bus = round(time_bus / 3600, 2)  # 乘车时间（分钟）

            cost_bus = result_bus['result']['routes'][0]['price']  # 乘车费用（元）

            diss_bus = str(km_bus) + '公里 ' + str(m_bus) + ' ' + str(timehour_bus) + '小时 ' + str(time_bus) + ' ' + str(
                cost_bus)

            print(diss_bus)

            diss = ori1 + ' ' + des1 + ' ' + diss_drive + ' ' + diss_ride + ' ' + diss_walk + ' ' + diss_bus

            print(diss)

            with open('./stimecol.txt', 'a', encoding='utf-8') as f:  # 保存路径

                f.write(diss)

                f.write('\n')

                f.close()

except:

    print('失败')

    pass



"""url有中文时的解决办法（重编码）

>>>import urllib

>>>name = u"北京西站"

>>>s = urllib.parse.quote(name)

>>>a = u"http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=EzdbUh0oh09KXdCoVfFDWSlANpQWcPFt"%(s)
"""


