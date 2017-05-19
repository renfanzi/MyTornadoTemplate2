#!/usr/bin/env python
# -*- coding:utf8 -*-
from controllers.home_handlers import BaseRequestHandler
import tornado
from tornado.web import RequestHandler
import json
import os
import random
import datetime, time
import requests
from common.base import result, MyGuid, my_datetime
from common.base import Config
from common.base import my_log
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from models.ProjectModel import SelectProInfor, SelectProInfor, SelectSbuProInfor, SelectQuestInfor, SelectSubQues, SelectAllVable
from core.ProjectDetailed import CreateProjectCore, CreateQuestCore, UploadSpssCore
import decimal




class CatProject(BaseRequestHandler):
    executor = ThreadPoolExecutor(2)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    def get(self):
        self.write("welcome ...11")

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        # 判断是否登录
        # 查看项目通过userid


        try:
            UserID = self.get_arguments("UserID")[0]
            res = SelectProInfor(UserID)
            for i in res:
                for k, va in i.items():
                    if isinstance(va, decimal.Decimal):
                        i[k] = str(va)
                    if isinstance(va, object):
                        i[k] = str(va)
            status=2000
        except Exception as e:
            my_log.error(e)
            res=""
            status = 5000

        # print(res)
        self.write(json.dumps(result(status=status, value=res)))
        self.finish()


# 需要用户id
class CreateProject(BaseRequestHandler):
    executor = ThreadPoolExecutor(2)
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    def get(self):
        self.write("welcome ...11")

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        # 判断是否登录
        # 查看项目通过userid
        # ret = CreateProjectCore(self)
        # CreateData = self.get_arguments("CreateData")
        # print(CreateData)
        # print(self.request.files["file"])

        try:
            ret = CreateProjectCore(self)
        except Exception as e:
            my_log.error(e)
            ret = 4002

        self.write(json.dumps(result(status=ret)))
        self.finish()


class CatSubProject(BaseRequestHandler):
    executor = ThreadPoolExecutor(2)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.write("welcome ...11")

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        # 判断是否登录
        # 查看项目通过userid

        try:
            ProjectID = self.get_arguments("ProjectID")[0]
            res = SelectSbuProInfor(ProjectID)
            for i in res:
                for k, va in i.items():
                    if isinstance(va, decimal.Decimal):
                        i[k] = str(va)
                    if isinstance(va, object):
                        i[k] = str(va)
            status = 2000
        except Exception as e:
            my_log.error(e)
            res = ""
            status = 5000

        self.write(json.dumps(result(status=status, value=res)))
        self.finish()


class CatQuest(BaseRequestHandler):
    executor = ThreadPoolExecutor(2)
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    def get(self):
        self.write("welcome ...11")

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        # 判断是否登录
        # 查看项目通过userid
        ProjectID = self.get_arguments("ProjectID")
        try:
            res = SelectQuestInfor(str(ProjectID[0]))
            for i in res:
                for k, va in i.items():
                    if isinstance(va, decimal.Decimal):
                        i[k] = str(va)
                    if isinstance(va, object):
                        i[k] = str(va)
            status = 2000
        except Exception as e:
            my_log.error(e)
            status = 4002
            res=None

        self.write(json.dumps(result(status=status, value={"data": res})))
        self.finish()


class CatSubQuest(BaseRequestHandler):
    executor = ThreadPoolExecutor(2)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.write("welcome ...11")

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        # 判断是否登录
        # 查看项目通过userid


        try:
            QuesID = self.get_arguments("QuesID")
            res = SelectSubQues(QuesID[0])
            allvalue = SelectAllVable(QuesID[0])
            if allvalue == 5002:
                allvalue=[]

            for i in res:
                for k, va in i.items():
                    if isinstance(va, decimal.Decimal):
                        i[k] = str(va)
                    if isinstance(va, object):
                        i[k] = str(va)
            status = 2000
        except Exception as e:
            my_log.error(e)
            status = 4002
            res = None
            allvalue = []

        self.write(json.dumps(result(status=status, value={"data": [res, allvalue]})))
        self.finish()


# 需要用户id, 项目id
class CreateQuest(BaseRequestHandler):
    executor = ThreadPoolExecutor(2)
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    def get(self):
        self.write("welcome ...11")

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        # res = CreateQuestCore(self)

        try:
            res = CreateQuestCore(self)

        except Exception as e:
            my_log.error(e)

            res=4002

        self.write(json.dumps(result(status=res)))
        self.finish()


# 需要用户id, 项目id, 问卷id
class UploadSpss(BaseRequestHandler):
    executor = ThreadPoolExecutor(2)
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    def get(self):
        self.write("welcome ...11")

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        # res = UploadSpssCore(self)
        try:
            res = UploadSpssCore(self)

        except Exception as e:
            my_log.error(e)

            res = 4003

        self.write(json.dumps(result(status=res)))
        self.finish()


# 查看所有标签的值
class CatSubVable(BaseRequestHandler):
    executor = ThreadPoolExecutor(2)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.write("welcome ...11")

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        # 判断是否登录
        # 查看项目通过userid

        try:
            DataTableID = self.get_arguments("DataTableID")[0]
            res = SelectSbuVable(DataTableID)
            status = 2000
        except Exception as e:
            my_log.error(e)
            res = ""
            status = 5000

        self.write(json.dumps(result(status=status, value={"data":res})))
        self.finish()