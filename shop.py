import urllib3
import json
import time
import random
import sys
import mysqldb

account_list = mysqldb.select_acc()

city_list = mysqldb.select_city()

cate_list = mysqldb.select_cate()

# 收集到的常用Header
my_headers = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
]


# 判断是否有手机号 粗略判断
def isphone(phone):
    if len(phone) == 11:
        return phone
    else:
        if '/' in phone:
            array = phone.split('/')
            for i in range(2):
                if len(array[i]) == 11:
                    return array[i]


# 请求url中包含城市ID
def geturl(cityid):
    url = "https://apimobile.meituan.com/group/v4/poi/pcsearch/" + cityid
    return url


# 请求头需要城市的简称
def getheaders(abbr, cookie):
    headers = {
        "User-Agent": random.choice(my_headers),
        "Referer": "https://" + abbr + ".meituan.com/",
        "Cookie": cookie,
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    return headers


# 请求参数 offset 偏移量  limit 大小  cateid 分类id
def getdate(uuid, userid, offset, limit, cate_id, token):
    data = {
        "uuid": uuid,
        "userid": userid,  # 用户ID需要修改
        "limit": limit,
        "offset": offset,
        "cateId": cate_id,
        "token": token,
        "areaId": -1
    }
    return data


def saveshop(city, cate, response):
    result = json.loads(response.data.decode('utf-8'))
    searchResult = result.get('data').get('searchResult')
    totalCount = result.get('data').get('totalCount')
    if totalCount > 0:
        for temp in searchResult:
            id = temp.get('id')
            title = temp.get('title')
            address = temp.get('address')
            phone = temp.get('phone')
            avgscore = temp.get('avgscore')  # 评分
            comments = temp.get('comments')  # 评论数
            historyCouponCount = temp.get('historyCouponCount')  # 历史成交单数
            # 判断是否有手机号
            phone_str = isphone(phone)
            if not phone_str is None:
                select_sql = "SELECT * FROM SHOP WHERE ID = " + str(id)
                flag = mysqldb.select(select_sql)
                if flag == 0:
                    insert_sql = "INSERT INTO SHOP VALUES (" + str(id) + "," \
                                 + "'" + title + "'," \
                                 + "'" + address + "'," \
                                 + "'" + phone_str + "'," \
                                 + str(city.cityid) + "," \
                                 + str(cate.cateid) + "," \
                                 + "'" + str(avgscore) + "'," \
                                 + str(comments) + "," \
                                 + str(historyCouponCount) + ",0)"
                    mysqldb.insert(insert_sql)
                else:
                    print('商家' + str(id) + '存在！！！')
    else:
        print(str(city.cityname) + "的分类" + str(cate.name) + "无数据")



for city in city_list:
    left = len(account_list) - 1
    account = account_list[random.randint(0, left)]
    # 创建http请求对象
    http = urllib3.PoolManager()
    for cate in cate_list:
        # 检查该城市的该分类记录是否满足
        select_shop_count_sql = "SELECT COUNT(*) FROM SHOP WHERE CITYID=" + str(city.cityid) + " AND CATEID=" + str(cate.cateid)
        count = mysqldb.select_shop_count(select_shop_count_sql)
        if count == 0:
            print(str(city.cityname) + "的分类" + str(cate.name) + "开始获取")
            url = geturl(str(city.cityid))
            fields = getdate(account.uuid, account.userid, 0, cate.count, cate.cateid, account.token)
            headers = getheaders(city.abbr, account.cookie)
            # 发送请求
            response = http.request('GET', url=url, fields=fields, headers=headers)
            if response.status == 200:
                print('数据正常,保存数据')
                saveshop(city, cate, response)
            else:
                print('******************error! system exit************************' + response.status)
                sys.exit()
            # 防止请求过多被封账号
            sleepTime = random.randint(1, 30)
            print('睡眠' + str(sleepTime) + '秒后开始')
            time.sleep(sleepTime)
