#!/usr/bin/env python
# -*- coding:utf-8 -*-

from controllers.proj_ques_handlers import CatProject, CreateProject, CatQuest, CreateQuest, UploadSpss, CatSubProject, CatSubQuest, CatSubVable
from controllers.proj_ques_handlers import MeanValues

urls = [
    # (r'/upload', Upload),

    # select all project of the user
    (r'/CatProject', CatProject),
    # create project and upload multi file
    (r'/CreateProject', CreateProject),

    (r'/CatSubProject', CatSubProject),# error create(cat)

    (r'/CatQuest', CatQuest),

    (r'/CatSubQuest', CatSubQuest),
    # create questionnaire
    (r'/CreateQuest', CreateQuest),
    # upload file of spss
    (r'/UploadSpss', UploadSpss),
    # questionnaire and variable details

    # 查看单个变量
    (r'/CatSubVable', CatSubVable),

    (r'/v1/MeanValues', MeanValues)

]