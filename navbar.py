from flask import Flask
from connect import yvt_connect
import pymysql

def populate_pools_session():
    pool_list = []
    conn = yvt_connect()
    curs = conn.cursor()

    sql = "select pool_name, id from prx_pool_group"
    curs.execute(sql)

    for j in curs:
        pool_list.append(j)

    conn.close
    return pool_list


def populate_proxy_session():

    proxy_list = []

    conn = yvt_connect()
    cur = conn.cursor()
    sql = "use koztel;"
    cur.execute(sql)

    cur.execute("select * from prx_pool_hostname")
    for j in cur:
        proxy_list.append(j)


    return proxy_list