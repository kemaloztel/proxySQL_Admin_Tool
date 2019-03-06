from flask import Flask
import pymysql
from connect import proxy_connect


def servers_print(host):
    server_list = []
    conn = proxy_connect(host)
    try:
        cur = conn.cursor()
        sql = "select *, hostgroup_id ||'_' || hostname || '_' || port as pk from mysql_servers"
        cur.execute(sql)

        for i in cur:
            server_list.append(i)

        conn.commit()
        return server_list

    except:
        pass

def users_print(host):
    user_list = []
    conn = proxy_connect(host)
    cur = conn.cursor()
    sql = "select *, username ||':' || backend || ':' || frontend as pk from mysql_users"
    cur.execute(sql)

    for j in cur:
        user_list.append(j)

    conn.commit()
    return user_list

def proxy_print(host):
    proxy_list = []
    conn = proxy_connect(host)
    cur = conn.cursor()
    sql = "select *, hostname ||'_' || port  as pk from proxysql_servers"
    cur.execute(sql)

    for k in cur:
        proxy_list.append(k)

    conn.commit()
    return proxy_list

