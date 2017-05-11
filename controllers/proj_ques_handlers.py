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
from common.base import result
from common.base import Config
from common.base import my_log
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor


class CatProject(BaseRequestHandler):
    executor = ThreadPoolExecutor(2)

    def get(self):
        self.write("welcome ...11")

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        # 判断是否登录
        # 查看项目通过userid
        self.write()
        self.finish()
