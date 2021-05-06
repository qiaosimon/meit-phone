import pymysql

# 获取连接
from bean.Account import Account
from bean.Cate import Cate
from bean.City import City


def open_conn():
    connect = pymysql.connect(host='localhost',  # 连接名称，默认127.0.0.1
                              user='phone',  # 用户名
                              passwd='phone',  # 密码
                              port=3306,  # 端口，默认为3306
                              db='phone',  # 数据库名称
                              charset='utf8'  # 字符编码
                              )
    return connect


# 插入数据
def insert(sql):
    connection = open_conn()
    cur = connection.cursor()
    try:
        cur.execute(sql)
        connection.commit()
    except:
        print('insert error:' + sql)
        connection.rollback()  # 如果发生错误则回滚
        return
    finally:
        cur.close()
        connection.close()


# 查询数据
def select(sql):
    connection = open_conn()
    cur = connection.cursor()
    flag = 0
    try:
        cur.execute(sql)  # 执行插入的sql语句
        data = cur.fetchall()
        for i in data[:]:
            flag = 1
        connection.commit()  # 提交到数据库执行
        return flag
    except:
        connection.rollback()  # 如果发生错误则回滚
        connection.close()  # 关闭数据库连接
        return flag
    finally:
        cur.close()
        connection.close()


def select_acc():
    sql = "SELECT * FROM ACCOUNT"
    connection = open_conn()
    cur = connection.cursor()
    try:
        cur.execute(sql)  # 执行插入的sql语句
        data = cur.fetchall()
        connection.commit()  # 提交到数据库执行
        list = []
        for row in data:
            account = Account(row[0], row[1],row[2],row[3])
            list.append(account)
        return list
    except:
        print('select account error :' + sql)
        connection.rollback()  # 如果发生错误则回滚
        return
    finally:
        cur.close()
        connection.close()


def select_city():
    sql = "SELECT * FROM CITY WHERE STATE = 1"
    connection = open_conn()
    cur = connection.cursor()
    try:
        cur.execute(sql)  # 执行插入的sql语句
        data = cur.fetchall()
        connection.commit()  # 提交到数据库执行
        list = []
        for row in data:
            city = City(row[0], row[1], row[2], row[3])
            list.append(city)
        return list
    except:
        print('select city error :' + sql)
        connection.rollback()  # 如果发生错误则回滚
        return
    finally:
        cur.close()
        connection.close()


def select_cate():
    sql = "SELECT * FROM CATE"
    connection = open_conn()
    cur = connection.cursor()
    try:
        cur.execute(sql)  # 执行插入的sql语句
        data = cur.fetchall()
        connection.commit()  # 提交到数据库执行
        list = []
        for row in data:
            cate = Cate(row[0], row[1], row[2])
            list.append(cate)
        return list
    except:
        print('select cate error :' + sql)
        connection.rollback()  # 如果发生错误则回滚
        return
    finally:
        cur.close()
        connection.close()


def select_shop_count(sql):
    connection = open_conn()
    cur = connection.cursor()
    try:
        cur.execute(sql)  # 执行
        count = cur.fetchall()[0][0]
        connection.commit()  # 提交到数据库执行
        return count
    except:
        print('select_shop_count error :' + sql)
        connection.rollback()  # 如果发生错误则回滚
        return
    finally:
        cur.close()
        connection.close()