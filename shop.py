import urllib3
import json
import time
import random
import sys
import mysqldb

account_list = mysqldb.select_acc()
print(account_list[0])

city_list = mysqldb.select_city()
print(city_list[0])

cate_list = mysqldb.select_cate()
print(cate_list[0])

# 收集到的常用Header
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
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
        "Cookie": cookie
    }
    return headers


# 请求参数 offset 偏移量  limit 大小  cateid 分类id
def getdate(userid, offset, limit, cate_id):
    data = {
        "uuid": "e3133799cc6743f9a6e5.1619677050.1.0.0",
        "userid": userid,  # 用户ID需要修改
        "limit": limit,
        "offset": offset,
        "cateId": cate_id,
        "token": "1acWPgfiHKPGQm8X4ObG6ibDMJsAAAAAZg0AAFxOWcY-6CsIuxnn2tRTiWcCUTMRz9pRrKQvvjEgAdkYBzM-oPefRDyGONc9emMq6Q",
        "areaId": -1
    }
    return data


def saveshop(cityid, cateid, response):
    result = json.loads(response.data.decode('utf-8'))
    searchResult = result.get('data').get('searchResult')
    # print(searchResult)
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
                insert_sql = "INSERT INTO SHOP VALUES (" + str(id) +"," \
                             + "'" + title +"'," \
                             + "'" + address + "'," \
                             + "'" + phone_str + "'," \
                             + str(city.cityid) + "," \
                             + str(cate.cateid) + "," \
                             + "'" + str(avgscore) + "'," \
                             + str(comments) + "," \
                             + str(historyCouponCount) + ")"
                mysqldb.insert(insert_sql)
            else:
                print('商家' + id + '存在！！！')


for city in city_list:
    left = len(account_list) - 1
    account = account_list[random.randint(0, left)]
    # 创建http请求对象
    http = urllib3.PoolManager()
    for cate in cate_list:
        # 检查该城市的该分类记录是否满足
        select_shop_count_sql = "SELECT COUNT(*) FROM SHOP WHERE CITYID=" + str(city.cityid) + " AND CATEID=" + str(cate.cateid)
        count = mysqldb.select_shop_count(select_shop_count_sql)
        if count < cate.count:
            url = geturl(str(city.cityid))
            fields = getdate(account.userid, 0, cate.count, cate.cateid)
            headers = getheaders(city.abbr, account.cookie)
            # 发送请求
            response = http.request('GET', url=url, fields=fields, headers=headers)
            if response.status == 200:
                print('数据正常,保存数据')
                saveshop(cate.cateid, cate.name, response)
            else:
                print('******************error! system exit************************')
                sys.exit()

            # 防止请求过多被封账号
            sleepTime = random.randint(1, 15)
            print('睡眠' + str(sleepTime) + '秒')
            time.sleep(sleepTime)
