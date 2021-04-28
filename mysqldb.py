import pymysql

# 获取连接
from Account import Account
from Cate import Cate
from City import City

def getconn():
    connect = pymysql.connect(host='localhost',  # 连接名称，默认127.0.0.1
                           user='nacos',  # 用户名
                           passwd='nacos',  # 密码
                           port=3306,  # 端口，默认为3306
                           db='nacos',  # 数据库名称
                           charset='utf8'  # 字符编码
                           )
    return connect

# 插入数据
def insert(sql):
    Connection = getconn()
    cur = Connection.cursor()
    try:
        cur.execute(sql)
        Connection.commit()
    except:
        print('insert error:' + sql)
        Connection.rollback()# 如果发生错误则回滚
        Connection.close() # 关闭数据库连接
        return
    finally:
        cur.close()
        Connection.close()

# 查询数据
def select(sql):
    Connection = getconn()
    cur = Connection.cursor()
    flag = 0
    try:
        cur.execute(sql) # 执行插入的sql语句
        data = cur.fetchall()
        for i in data[:]:
            print (i)
            flag = 1
        Connection.commit() # 提交到数据库执行
        return flag
    except:
        Connection.rollback()# 如果发生错误则回滚
        Connection.close() # 关闭数据库连接
        return flag
    finally:
        cur.close()
        Connection.close()



def selectacc():
    sql  = "SELECT * FROM ACCOUNT"
    Connection = getconn()
    cur = Connection.cursor()
    try:
        cur.execute(sql) # 执行插入的sql语句
        data = cur.fetchall()
        Connection.commit() # 提交到数据库执行
        list = []
        for row in data:
            account = Account(row[0],row[1])
            list.append(account)
        return list
    except:
        print('select account error :' + sql)
        Connection.rollback()# 如果发生错误则回滚
        return
    finally:
        cur.close()
        Connection.close()

def selectcity():
    sql  = "SELECT * FROM CITY WHERE STATE = 1"
    Connection = getconn()
    cur = Connection.cursor()
    try:
        cur.execute(sql) # 执行插入的sql语句
        data = cur.fetchall()
        Connection.commit() # 提交到数据库执行
        list = []
        for row in data:
            city = City(row[0],row[1],row[2],row[3])
            list.append(city)
        return list
    except:
        print('select city error :' + sql)
        Connection.rollback()# 如果发生错误则回滚
        return
    finally:
        cur.close()
        Connection.close()


def selectcate():
    sql  = "SELECT * FROM CATE"
    Connection = getconn()
    cur = Connection.cursor()
    try:
        cur.execute(sql) # 执行插入的sql语句
        data = cur.fetchall()
        Connection.commit() # 提交到数据库执行
        list = []
        for row in data:
            cate = Cate(row[0],row[1],row[2])
            list.append(cate)
        return list
    except:
        print('select cate error :' + sql)
        Connection.rollback()# 如果发生错误则回滚
        return
    finally:
        cur.close()
        Connection.close()