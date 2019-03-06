from flask import Flask, session
from connect import proxy_connect


def adduser(form):
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'INSERT INTO mysql_users (username, password, active, use_ssl, default_hostgroup, default_schema, schema_locked, transaction_persistent,fast_forward, backend, frontend, max_connections) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    cur.execute(sql, (form.username.data,
                      form.password.data,
                      form.active.data,
                      form.use_ssl.data,
                      form.default_hostgroup.data,
                      form.default_schema.data,
                      form.schema_locked.data,
                      form.transaction_persistent.data,
                      form.fast_forward.data,
                      form.backend.data,
                      form.frontend.data,
                      form.max_connections.data
                      )
                )

    conn.commit()



def rmuser(a, b, c):
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'DELETE FROM mysql_users WHERE username=%s and backend=%s and frontend=%s'

    cur.execute(sql, (a, b, c))
    conn.commit()
    conn.close()


def activeuser(a, b, c):
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'UPDATE mysql_users SET active=1 WHERE username=%s and  backend=%s and frontend=%s'

    cur.execute(sql, (a, b, c))
    conn.commit()
    conn.close()


def deactiveuser(a, b, c):
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'UPDATE mysql_users SET active=0 WHERE username=%s and  backend=%s and frontend=%s'

    cur.execute(sql, (a, b, c))
    conn.commit()
    conn.close()


def veri_ekle(form):
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = "INSERT INTO author (username,email,password) VALUES (%s,%s,%s)"

    try:
        cur.execute(sql,
                    (form.username.data,
                     form.email.data,
                     form.password.data
                     )
                    )
        conn.commit()
    except Exception as e:
        print("Exception olustu:", e)
        conn.rollback()
        return False


def user_config_load():
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'LOAD MYSQL USERS TO RUNTIME'

    cur.execute(sql)
    conn.commit()
    conn.close


def user_config_save():
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'SAVE MYSQL USERS TO DISK'

    cur.execute(sql)
    conn.commit()
    conn.close

def update_user(form, username, backend, frontend):
    x = session.get('host', 'not set')
    conn = proxy_connect(x)
    cur = conn.cursor()

    sql = 'UPDATE mysql_users SET username=%s, password=%s, active=%s, use_ssl=%s, default_hostgroup=%s, ' \
          'default_schema=%s, schema_locked=%s, transaction_persistent=%s, fast_forward=%s, backend=%s, ' \
          'frontend=%s, max_connections=%s WHERE username=%s and backend=%s and frontend=%s'

    cur.execute(sql, (form.username.data,
                       form.password.data,
                       form.active.data,
                       form.use_ssl.data,
                       form.default_hostgroup.data,
                       form.default_schema.data,
                       form.schema_locked.data,
                       form.transaction_persistent.data,
                       form.fast_forward.data,
                       form.backend.data,
                       form.frontend.data,
                       form.max_connections.data,
                       username,
                       backend,
                       frontend
                       )
                 )

    conn.commit()
    conn.close