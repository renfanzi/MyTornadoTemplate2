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
from models.ProjectModel import SelectProInfor, SelectProInfor, SelectSbuProInfor, SelectQuestInfor, SelectSubQues
from models.ProjectModel import  SelectAllVable, SelectDataTablesInfo, SelectVarNameInfo, SelectVarNameData
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
            res=""

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
            if QuesID:
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
            else:
                status = 4002
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
            if res[0] == 2000:
                quesid = res[1]
            else:
                quesid = ""
        except Exception as e:
            my_log.error(e)
            quesid = ""
            res=4002

        self.write(json.dumps(result(status=res, value=quesid)))
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


# 查看标签的值info
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
            QuesID = self.get_arguments("QuesID")[0]
            VarName = self.get_arguments("VarName")[0]
            if QuesID and ValueError:
                meta_data_tables = SelectDataTablesInfo(QuesID)
                if meta_data_tables:
                    if len(meta_data_tables) == 1:
                        DataTableID = meta_data_tables[0]["DataTableID"]
                        DataTableName = meta_data_tables[0]["DataTableName"]
                        sub_varname_info = SelectVarNameInfo(DataTableID, VarName)
                        VarLabel = sub_varname_info["VarLabel"]
                        VarValues = json.loads(sub_varname_info["VarValues"])


                        df = SelectVarNameData(VarName, DataTableName)
                        effective_total = len(df.dropna())
                        all_total = len(df)
                        if isinstance(VarValues, dict):
                            var_dict = (df.groupby(VarName).size()).to_json()

                        else:
                            var_dict = ""
                        status = 2000
                        res = {"VarName": VarName, "VarLabel": VarLabel, "VarValues": VarValues, "effective_total": effective_total, "all_total": all_total, "data_summary": var_dict}

                else:
                    status = 4002
                    res = ""
            else:
                status = 4002
                res = ""
        except Exception as e:
            my_log.error(e)
            res = ""
            status = 5000

        self.write(json.dumps(result(status=status, value={"data":res})))
        self.finish()


class MeanValues(BaseRequestHandler):
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
            QuesID = self.get_arguments("QuesID")[0]
            VarName = self.get_arguments("VarName")[0]
            if QuesID and ValueError:
                # 表的信息
                meta_data_tables = SelectDataTablesInfo(QuesID)
                if meta_data_tables:
                    if len(meta_data_tables) == 1:
                        DataTableID = meta_data_tables[0]["DataTableID"]
                        DataTableName = meta_data_tables[0]["DataTableName"]
                        # 变量的信息
                        sub_varname_info = SelectVarNameInfo(DataTableID, VarName)
                        VarValues = sub_varname_info["VarValues"]
                        # 变量的数据
                        df = SelectVarNameData(VarName, DataTableName)
                        SendDict = {}
                        SendDict["columnID"] = VarName
                        SendDict["countN"] = len(df.dropna())
                        SendDict["maxValue"] = str(dict(df.max())[VarName])
                        SendDict["minValue"] = str(dict(df.min())[VarName])
                        SendDict["average"] = str(dict(df.mean())[VarName])
                        SendDict["stdev"] = str(dict(df.std())[VarName])
                        SendDict["sum"] = str(dict(df.sum())[VarName])
                        SendDict["midValue"] = str(dict(df.median())[VarName])

                        # print(SendDict)
                        status = 2000
                        res = SendDict

                else:
                    status = 4002
                    res = ""
            else:
                status = 4002
                res = ""
        except Exception as e:
            my_log.error(e)
            res = ""
            status = 5000

        self.write(json.dumps(result(status=status, value={"data":res})))
        self.finish()
