from flask import Flask, render_template
import pymysql


def proxy_connect(host):
    return pymysql.connect(host=host, port=6032, user='koztel', passwd='qwerty')


def yvt_connect():
    return pymysql.connect(host='secret', db='...', port=3306, user='koztel', passwd='qwerty')
