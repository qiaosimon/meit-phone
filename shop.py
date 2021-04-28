import urllib3
import json
import openpyxl
import time
import random
import sys
import mysqldb


accountlist = mysqldb.selectacc()
print(accountlist[0])

citylist = mysqldb.selectcity()
print(citylist[0])


catelist = mysqldb.selectcate()
print(catelist[0])

insertsql = "INSERT INTO SHOP VALUES ('1','AA','SS','123',1,2,'4.5',1,1)"

#mysqldb.insert(insertsql)

selectsql = "SELECT * FROM SHOP WHERE ID = 1"

flag = mysqldb.select(selectsql)
print(flag)