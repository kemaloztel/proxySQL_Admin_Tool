from flask import Flask, json, session
from connect import proxy_connect


def add(form):
    x = session.get ('host', 'not set')
    print ("serveroperation x: ")
    print (x)
    conn = proxy_connect (x)
    cur = conn.cursor ()

    sql = 'INSERT INTO mysql_servers (hostgroup_id, hostname, port, status, weight, compression, max_connections, max_replication_lag,use_ssl, max_latency_ms, comment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    cur.execute (sql, (form.hostgroup_id.data,
                       form.hostname.data,
                       form.port.data,
                       form.status.data,
                       form.weight.data,
                       form.compression.data,
                       form.max_connections.data,
                       form.max_replication_lag.data,
                       form.use_ssl.data,
                       form.max_latency_ms.data,
                       form.comment.data
                       )
                 )

    conn.commit ()


def clear(a, b, c):
    x = session.get ('host', 'not set')
    conn = proxy_connect (x)
    cur = conn.cursor ()

    sql = 'DELETE FROM mysql_servers WHERE hostgroup_id=%s and hostname=%s and port=%s'
    cur.execute (sql, (a, b, c))

    conn.commit ()


def cevrimici(a, b, c):
    x = session.get ('host', 'not set')
    conn = proxy_connect (x)
    cur = conn.cursor ()

    sql = 'UPDATE mysql_servers SET status="ONLINE" WHERE hostgroup_id=%s and hostname=%s and port=%s'
    cur.execute (sql, (a, b, c))

    conn.commit ()


def offlinesoft(a, b, c):
    x = session.get ('host', 'not set')
    conn = proxy_connect (x)
    cur = conn.cursor ()

    sql = 'UPDATE mysql_servers SET status="OFFLINE_SOFT" WHERE hostgroup_id=%s and hostname=%s and port=%s'
    cur.execute (sql, (a, b, c))

    conn.commit ()
    conn.close ()


def offlinehard(a, b, c):
    x = session.get ('host', 'not set')
    conn = proxy_connect (x)
    cur = conn.cursor ()

    sql = 'UPDATE mysql_servers SET status="OFFLINE_HARD" WHERE hostgroup_id=%s and hostname=%s and port=%s'
    cur.execute (sql, (a, b, c))

    conn.commit ()
    conn.close ()


def server_config_load():
    x = session.get ('host', 'not set')
    conn = proxy_connect (x)
    cur = conn.cursor ()

    sql = 'LOAD MYSQL SERVERS TO RUNTIME'

    cur.execute (sql)
    conn.commit ()
    conn.close


def server_config_save():
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'SAVE MYSQL SERVERS TO DISK'

    cur.execute(sql)
    conn.commit()
    conn.close


def update_server(form, a, b, c):
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'UPDATE mysql_servers SET hostgroup_id=%s, hostname=%s, port=%s, status=%s, weight=%s, compression=%s, ' \
          'max_connections=%s, max_replication_lag=%s, use_ssl=%s, max_latency_ms=%s, comment=%s ' \
          'WHERE hostgroup_id=%s and hostname=%s and port=%s'

    cur.execute (sql, (form.hostgroup_id.data,
                       form.hostname.data,
                       form.port.data,
                       form.status.data,
                       form.weight.data,
                       form.compression.data,
                       form.max_connections.data,
                       form.max_replication_lag.data,
                       form.use_ssl.data,
                       form.max_latency_ms.data,
                       form.comment.data,
                       a,
                       b,
                       c
                       )
                 )

    conn.commit()
    conn.close
