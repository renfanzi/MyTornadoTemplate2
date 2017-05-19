#!/usr/bin/env python
# -*- coding:utf-8 -*-

from common.base import result, MyGuid, my_datetime
from common.base import Config
from common.base import my_log
import json
import os, re
import random
import datetime, time
import requests
import hashlib

from models.ProjectModel import CreateMetaProj, CreateMetaProInfo, CreateMetaProFIles, CreateMetaProUsers
from models.ProjectModel import SelectProFile, CreateQuest, CreateQuestFile, CreateQuestInfo, CreateQuestUsers
from core.UploadSpss import upload_spss


def CreateProjectCore(self):
    CreateData = self.get_arguments("CreateData")

    if len(CreateData) == 1:
        CreateData = json.loads(CreateData[0], encoding='utf-8')
        print(CreateData)
        if (len(CreateData) == 18):  # 数据库共17个值
            ProjectID = MyGuid()
            UserID = CreateData["UserID"]

            ProjectName = CreateData["ProjectName"]
            ProjectOrgan = CreateData["ProjectOrgan"]
            ProjectSubject = CreateData["ProjectSubject"]
            SubjectField = int(CreateData["SubjectField"])
            ProjectLevel = CreateData["ProjectLevel"]

            ProjectSource = CreateData["ProjectSource"]
            FundsSource = CreateData["FundsSource"]
            ProjectSummary = CreateData["ProjectSummary"]
            CycleType = CreateData["CycleType"]
            CycleSpan = CreateData["CycleSpan"]

            TeamIntroduction = CreateData["TeamIntroduction"]
            ProjectPublic = CreateData["ProjectPublic"]  # 公开性
            ProjectStatus = 1 # 状态

            EditUserID = UserID
            EditTime = str(datetime.datetime.now())
            CreateTime = str(datetime.datetime.now())


        else:
            return 4002

        # -----------------------------------project_info

        InfoTile = CreateData["InfoTile"]
        InfoContent = CreateData['InfoContent']

        Pi_EditUserID = UserID
        Pi_EditTime = str(datetime.datetime.now())


    else:
        return 4002

        # ------------------------------------project_files
    # try:

    AuthorUserIDs = None
    FilePublic = 1
    UploadUserID = UserID
    UploadTime = CreateTime
    FIleStatus = 1
    FileEditUserID = UserID

    project_data = {}
    project_data["ProjectID"] = ProjectID
    project_data["UserID"] = UserID
    project_data["ProjectName"] = ProjectName
    project_data["ProjectOrgan"] = ProjectOrgan
    project_data["ProjectSubject"] = ProjectSubject
    project_data["SubjectField"] = SubjectField
    project_data["ProjectLevel"] = ProjectLevel
    project_data["ProjectSource"] = ProjectSource
    project_data["FundsSource"] = FundsSource
    project_data["ProjectSummary"] = ProjectSummary
    project_data["CycleType"] = CycleType
    project_data["CycleSpan"] = CycleSpan
    project_data["TeamIntroduction"] = TeamIntroduction
    project_data["ProjectPublic"] = ProjectPublic
    project_data["ProjectStatus"] = ProjectStatus
    project_data["EditUserID"] = EditUserID
    project_data["EditTime"] = EditTime
    project_data["CreateTime"] = CreateTime

    CreateMetaProj(project_data)


    project_info_data = {"ProjectID":ProjectID, "InfoTile":InfoTile, "InfoContent":InfoContent,
                         "EditUserID":Pi_EditUserID, "EditTime":Pi_EditTime, "CreateTime":CreateTime}
    print(project_info_data)
    CreateMetaProInfo(project_info_data)

    if CreateData["Isfile"] == "1":

        file_metas = self.request.files["file"]
        pi_file_type = []
        pi_file_path = []
        md5_li = []
        import hashlib


        for meta in range(len(file_metas)):
            md5_value = hashlib.md5()
            file_name = file_metas[meta]['filename']
            FileType = file_name.split(".")[-1]
            pi_file_type.append(FileType)
            # 这块对路径的修改和文件目录的创建
            if (Config().get_content('filepath')['upload_path']):
                file_path = Config().get_content('filepath')['upload_path']
            else:
                file_path = os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'file'))

            # 判断file_path 下面有没有user_id 文件目录, 没有创建一个
            user_path = os.path.join(file_path, str(UserID))
            user_proje = os.path.join(user_path, ProjectID)
            # 判断用户目录,
            if not os.path.exists(user_path):
                os.makedirs(user_path)
            # 其次是项目
            if not os.path.exists(user_proje):
                os.makedirs(user_proje)
            # 重复的话备份一次
            if os.path.exists(os.path.join(user_proje, file_name)):
                os.renames(os.path.join(user_proje, file_name), os.path.join(user_proje, file_name + ".bak"))
            pi_file_path.append(os.path.join(user_proje, file_name))
            # file_path = os.path.join("file", file_name)
            # write input file --file
            FilePath = os.path.join(user_proje, file_name)
            with open(FilePath, 'wb+') as up:
                up.write(file_metas[meta]['body'])

            md5_value.update(file_metas[meta]['body'])
            FileMd5 = md5_value.hexdigest()
            md5_li.append(FileMd5)
            if len(file_metas) == 1:
                FileTile = CreateData["FileTile"]
                FileDescript = CreateData["FileDescript"]
            else:
                FileTile = CreateData["FileTile"][meta]
                FileDescript = CreateData["FileDescript"][meta]

            project_files_data = {"ProjectID":ProjectID, "FileTile":FileTile, "FileDescript":FileDescript,
                                  "FileType":FileType, "FilePath":FilePath, "FilePublic":FilePublic, "AuthorUserIDs":AuthorUserIDs,
                                  "UploadUserID":UploadUserID, "UploadTime":UploadTime, "FileMd5":FileMd5,
                                  "FIleStatus":FIleStatus, "EditUserID":EditUserID, "EditTime":EditTime}
            CreateMetaProFIles(project_files_data)


    # -------------------project users
    UserRole = 99
    UserStatus = 1
    project_users = {"ProjectID":ProjectID, "UserID":UserID, "UserRole":UserRole, "UserStatus":UserStatus}
    CreateMetaProUsers(project_users)

    # except Exception as e:
    #     my_log.error(e)
    #     return 4002

    return 2000


def CreateQuestCore(self):
    try:
        CreateData = self.get_arguments("CreateData")
        print(CreateData)
        if (len(CreateData) == 1):
            CreateData = json.loads(CreateData[0], encoding='utf-8')
            if (len(CreateData) == 17):
                QuesID = MyGuid()
                ProjectID = CreateData["ProjectID"]
                QuesTitle = CreateData["QuesTitle"]
                QuesLeads = CreateData["QuesLeads"]
                Respondents = CreateData["Respondents"]
                SurveyType = int(CreateData["SurveyType"])
                SamplePlan = CreateData["SamplePlan"]
                SampleRepresentation = CreateData["SampleRepresentation"]
                ImplementOrgan = CreateData["ImplementOrgan"]
                ImplementTime = str(CreateData["ImplementTime"])
                DataChannel = int(CreateData["DataChannel"])

                DataSource = CreateData["DataSource"]
                QuesStatus = 1
                CreateTime = str(datetime.datetime.now())
                InfoTile = CreateData["InfoTile"]
                InfoContent = CreateData["InfoContent"]
                EditUserID = CreateData["UserID"]
                EditTime = str(datetime.datetime.now())

            else:
                return 4002


        else:
            return 4002
        QuestData = {"QuesID": QuesID, "ProjectID": ProjectID, "QuesTitle": QuesTitle, "QuesLeads": QuesLeads,"Respondents": Respondents,
                     "SurveyType": SurveyType, "SamplePlan": SamplePlan, "SampleRepresentation": SampleRepresentation,
                     "ImplementOrgan": ImplementOrgan, "ImplementTime": ImplementTime, "DataChannel": DataChannel,
                     "DataSource": DataSource, "QuesStatus": QuesStatus, "CreateTime": CreateTime}
        CreateQuest(QuestData)

        QuestInfoData = {"QuesID": QuesID, "InfoTile":InfoTile, "InfoContent": InfoContent, "EditUserID": EditUserID,
                         "EditTime": EditTime, "CreateTime": CreateTime}
        CreateQuestInfo(QuestInfoData)
        file_metas = self.request.files["file"]
        FilePublic=1
        UserID = UploadUserID = AuthorUserIDs = EditUserID
        FileStatus = 1
        UploadTime = str(datetime.datetime.now())
        if CreateData["Isfile"] == '1':
            for meta in range(len(file_metas)):
                md5_value = hashlib.md5()
                file_name = file_metas[meta]['filename']
                FileType = file_name.split(".")[-1]

                if (Config().get_content('filepath')['upload_path']):
                    file_path = Config().get_content('filepath')['upload_path']
                else:
                    file_path = os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'file'))

                # 判断file_path 下面有没有user_id 文件目录, 没有创建一个
                user_path = os.path.join(file_path, str(UserID))
                user_proje = os.path.join(user_path, ProjectID)
                # 判断用户目录,
                if not os.path.exists(user_path):
                    os.makedirs(user_path)
                file_que_path = os.path.join(user_proje, QuesID)
                if not os.path.exists(file_que_path):
                    os.makedirs(file_que_path)
                # 重复的话备份一次

                FilePath = os.path.join(file_que_path, file_name)
                with open(FilePath, 'wb+') as up:
                    up.write(file_metas[meta]['body'])

                md5_value.update(file_metas[meta]['body'])
                FileMD5 = md5_value.hexdigest()
                if len(file_metas) == 1:
                    FileTile = CreateData["FileTile"]
                    FileDescript = CreateData["FileDescript"]
                else:
                    FileTile = CreateData["FileTile"][meta]
                    FileDescript = CreateData["FileDescript"][meta]
                # project_files_data = {}
                project_files_data = {"ProjectID": ProjectID, "FileTile": FileTile, "FileDescript": FileDescript,
                                      "FileType": FileType, "FilePath": FilePath, "FilePublic": FilePublic,
                                      "AuthorUserIDs": AuthorUserIDs,
                                      "UploadUserID": UploadUserID, "UploadTime": UploadTime, "FileMd5": FileMD5,
                                      "FIleStatus": 1, "EditUserID": EditUserID, "EditTime": EditTime}
                CreateMetaProFIles(project_files_data)
                QuestFile = {"QuesID": QuesID, "FileTile": FileTile, "FileDescript": FileDescript, "FileType": FileType,
                             "FilePath": FilePath, "FilePublic": FilePublic, "AuthorUserIDs": AuthorUserIDs, "UploadUserID": UploadUserID,
                             "UploadTime": UploadTime, "FileMD5": FileMD5, "FileStatus": FileStatus, "EditTime": EditTime}
                CreateQuestFile(QuestFile)

        UserRole=2
        UserPrivilege = None
        UserStatus = 1
        QuestUser = {"QuesID": QuesID, "UserID": UserID, "UserRole":UserRole, "UserPrivilege":UserPrivilege, "UserStatus": UserStatus, "CreateTime": CreateTime}
        CreateQuestUsers(QuestUser)
    except Exception as e:
        my_log.error(e)
        return 4002
    return 2000


def UploadSpssCore(self):
    file_metas = self.request.files["FileSpss"]
    UserID = self.get_arguments("UserID")[0]
    ProjectID = self.get_arguments("ProjectID")[0]
    QuesID = self.get_arguments("QuesID")[0]
    # print(UserID)

    if not (UserID and ProjectID and QuesID):

        return 4000
    if len(file_metas) == 1:
        FileTile = None
        FileDescript = None
        FileType = ".sav"
        FilePublic = 1
        AuthorUserIDs = ""
        UploadUserID = UserID
        UploadTime = EditTime = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        FileStatus = 1
        DataTableID = ""

        print(file_metas)

        for meta in file_metas:
            md5_value = hashlib.md5()
            file_name = meta['filename']
            if file_name.split(".")[-1] != "sav":
                # self.write(json.dumps(result(4000, value=None), ensure_ascii=False))

                return 4000
                break
            # 这块对路径的修改和文件目录的创建
            if (Config().get_content('filepath')['upload_path']):
                file_path = Config().get_content('filepath')['upload_path']
            else:
                file_path = os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'file'))

            # 用户目录
            user_path = os.path.join(file_path, str(UserID))
            # 项目目录
            user_proje = os.path.join(user_path, ProjectID)
            # 判断用户目录,
            if not os.path.exists(user_path):
                os.makedirs(user_path)
            # 其次是项目
            if not os.path.exists(user_proje):
                os.makedirs(user_proje)
            # 问卷目录
            user_ques = os.path.join(user_proje, QuesID)
            if not os.path.exists(user_ques):
                os.makedirs(user_ques)
            # 重复的话备份一次
            if os.path.exists(os.path.join(user_ques, file_name)):
                os.renames(os.path.join(user_ques, file_name), os.path.join(user_ques, file_name + ".bak"))

            FilePath = os.path.join(user_ques, file_name)

            # file_path = os.path.join("file", file_name)
            # write input file --file
            with open(FilePath, 'wb') as up:
                up.write(meta['body'])
            md5_value.update(meta['body'])
            FileMD5 = md5_value.hexdigest()

            QuestFile = {"QuesID": QuesID, "FileTile": FileTile, "FileDescript": FileDescript, "FileType": FileType,
                         "FilePath": FilePath, "FilePublic": FilePublic, "AuthorUserIDs": AuthorUserIDs,
                         "UploadUserID": UploadUserID,
                         "UploadTime": UploadTime, "FileMD5": FileMD5, "FileStatus": FileStatus, "EditTime": EditTime}

            CreateQuestFile(QuestFile)
            upload_spss().main(FilePath, file_name, UserID, QuesID)


        return 2000
    else:
        return 4003

