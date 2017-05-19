#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql
import os
import configparser
from common.base import my_log, Config
import datetime, time, uuid, re

'''
class Config(object):
    """
    # Config().get_content("user_information")
    """

    def __init__(self, config_filename="zk_css.cnf"):
        # file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_filename)
        file_path = config_filename
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


class base_pymysql(object):
    def __init__(self, host, port, user, password, db_name):
        self.db_host = host
        self.db_port = int(port)
        self.user = user
        self.password = str(password)
        self.db = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = pymysql.connect(host=self.db_host, port=self.db_port, user=self.user, passwd=self.password, db=self.db, charset="utf8")
        # self.conn = pymysql.connect(host='192.168.72.135', port=3306, user='root', passwd='123456', db='test', charset="utf8")
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)




class My_Pymysql(base_pymysql):
    """
    Basic Usage:

        ret = My_Pymysql('test1')
        res = ret.selectone_sql("select * from aaa")
        print(res)
        ret.close()
    Precautions:
        Config.__init__(self, config_filename="zk_css.cnf")

    """
    def __init__(self, conf_name):
        self.conf = Config().get_content(conf_name)
        super(My_Pymysql, self).__init__(**self.conf)
        self.connect()

    def idu_sql(self, sql):
        # adu: insert, delete, update的简写
        # 考虑到多语句循环, try就不写在这里了
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_sql(self, sql, value=None):
        # adu: insert, delete, update的简写
        self.cursor.execute(sql, value)
        self.conn.commit()

    def selectone_sql(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.fetchone()

    def selectall_sql(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
        self.conn = None
        self.cursor = None
'''

'''
import datetime, time, uuid, re

date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

us = ("%.7f" % time.time())[-7:]

res  = "".join(re.findall('\d+', str(uuid.uuid4())))[:7]

ret = date +  us + res
print(ret)
print(len(ret))
'''


