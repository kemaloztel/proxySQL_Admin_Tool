from flask import Flask, session
from connect import proxy_connect


def proxy_config_save():
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'SAVE MYSQL USERS TO DISK'

    cur.execute(sql)
    conn.commit()
    conn.close


def proxy_config_load():
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'LOAD MYSQL USERS TO RUNTIME'

    cur.execute(sql)
    conn.commit()
    conn.close


def remove_proxy(a, b):
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'DELETE FROM proxysql_servers WHERE hostname=%s and port=%s'

    cur.execute(sql, (a, b))
    conn.commit()
    conn.close


def add_proxy(form):
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'INSERT INTO proxysql_servers (hostname, port, weight, comment) VALUES (%s,%s,%s,%s)'

    cur.execute(sql, (form.hostname.data,
                       form.port.data,
                       form.weight.data,
                       form.comment.data
                       )
                )

    conn.commit()
    conn.close


def update_proxy(form, a, b):
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'UPDATE proxysql_servers SET hostname=%s, port=%s, weight=%s, comment=%s WHERE hostname=%s and port=%s'

    cur.execute(sql, (form.hostname.data,
                      form.port.data,
                      form.weight.data,
                      form.comment.data,
                      a,
                      b
                     )
                )

    conn.commit()
    conn.close
