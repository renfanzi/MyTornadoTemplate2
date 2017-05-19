#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
from common.base import MyPymysql, MyGuid, my_datetime, my_log


def SelectProInfor(UserId):
    sql = "select `ProjectID`, `ProjectName` from `meta_project` where UserID=%s" % UserId
    ret = MyPymysql('metadata')
    res = ret.selectall_sql(sql)
    ret.close()

    return res


def SelectSbuProInfor(ProjectID):
    ProjSql = "SELECT a.*, b.*, c.* ,d.*  FROM meta_project a, meta_project_info b, meta_project_users c, meta_project_files d " \
              "WHERE a.ProjectID = b.ProjectID AND a.ProjectID = c.ProjectID AND a.ProjectID = d.ProjectID AND a.ProjectID='{}';".format(
        ProjectID)
    ret = MyPymysql('metadata')
    ProjData = ret.selectall_sql(ProjSql)
    res = ProjData
    ret.close()
    return res


def CreateMetaProj(data):
    # data = ('121212', '12121212', 'aaa', 'aa', 'aa', 1, 1, 1, 1, '11', 1, 111.0, '111', 1, 1, '111', '2012-10-10')

    sql = "insert into `meta_project` SET ProjectID={}, UserID={}, ProjectName='{}', ProjectOrgan='{}', ProjectSubject='{}', " \
          "SubjectField={}, ProjectLevel={}, ProjectSource={}, FundsSource={}, ProjectSummary='{}', CycleType={}, CycleSpan='{}', " \
          "TeamIntroduction='{}', ProjectPublic={}, ProjectStatus={}, EditUserID={};".format(
        data["ProjectID"],
        data["UserID"],
        data["ProjectName"],
        data["ProjectOrgan"],
        data["ProjectSubject"],
        data["SubjectField"],
        data["ProjectLevel"],
        data["ProjectSource"],
        data["FundsSource"],
        data["ProjectSummary"],
        data["CycleType"],
        int(data["CycleSpan"]),
        data["TeamIntroduction"],
        data["ProjectPublic"],
        data["ProjectStatus"],
        data["EditUserID"])
    # print(sql)
    ret = MyPymysql('metadata')
    ret.idu_sql(sql)
    ret.close()


def CreateMetaProInfo(data):
    # project_info_data = {"ProjectID": ProjectID, "InfoTile": InfoTile, "InfoContent": InfoContent,
    #                      "EditUserID": Pi_EditUserID, "EditTime": Pi_EditTime, "CreateTime": CreateTime}
    sql = "insert into `meta_project_info` SET ProjectID={}, InfoTile='{}', InfoContent='{}', EditUserID={}".format(
        data["ProjectID"],
        data["InfoTile"],
        data["InfoContent"],
        data["EditUserID"])
    # print(sql)
    ret = MyPymysql('metadata')
    ret.idu_sql(sql)
    ret.close()


def CreateMetaProFIles(data):
    # project_files_data = {"ProjectID": ProjectID, "FileTile": FileTile, "FileDescript": FileDescript,
    #                       "FileType": FileType, "FilePath": FilePath, "FilePublic": FilePublic,
    #                       "AuthorUserIDs": AuthorUserIDs,
    #                       "UploadUserID": UploadUserID, "UploadTime": UploadTime, "FileMd5": FileMd5,
    #                       "FIleStatus": FIleStatus, "EditUserID": EditUserID, "EditTime": EditTime}

    sql = "insert into `meta_project_files`  SET ProjectID={}, FileTile='{}', FileDescript='{}',FileType='{}', FilePath='{}', " \
          "FilePublic={},AuthorUserIDs='{}',UploadUserID='{}', FileMd5='{}',FIleStatus={}, EditUserID='{}';".format(
        data["ProjectID"],
        data["FileTile"],
        data["FileDescript"],
        data["FileType"],
        data["FilePath"],
        data["FilePublic"],
        data["AuthorUserIDs"],
        data["UploadUserID"],
        data["FileMd5"],
        data["FIleStatus"],
        data["EditUserID"])

    # print(sql)
    ret = MyPymysql('metadata')
    ret.idu_sql(sql)
    ret.close()


def CreateMetaProUsers(data):
    # project_users = {"ProjectID": ProjectID, "UserID": UserID, "UserRole": UserRole, "UserStatus": UserStatus,
    #                  "CreateTime": CreateTime}
    sql = "insert into `meta_project_users` SET ProjectID={}, UserID={}, UserRole={}, UserStatus={}".format(
        data["ProjectID"], data["UserID"], data["UserRole"], data["UserStatus"])
    ret = MyPymysql('metadata')
    ret.idu_sql(sql)
    ret.close()


def SelectProFile(project_id):
    sql = "select FilePath from `meta_project_files` WHERE ProjectID={}".format(project_id)
    ret = MyPymysql('metadata')
    # print(sql)
    res = ret.selectall_sql(sql)
    # print(res)
    ret.close()
    return res


# -------------------------


def SelectQuestInfor(ProjectID):
    sql = "select `QuesID`, `ProjectID`, `QuesTitle`, `QuesLEads` from `meta_questionnaire` where ProjectID=%s AND QuesStatus=1 " % ProjectID
    ret = MyPymysql('metadata')
    res = ret.selectall_sql(sql)
    ret.close()
    return res


def SelectSubQues(QuesID):
    QuesSql = "SELECT a.*, b.*, c.* ,d.*  FROM meta_questionnaire a, meta_questionnaire_files b, " \
              "meta_questionnaire_info c, meta_questionnaire_users d " \
              "WHERE a.QuesID = b.QuesID AND a.QuesID = c.QuesID AND a.QuesID = d.QuesID  AND a.QuesID='{}';".format(
        QuesID)
    ret = MyPymysql('metadata')
    QuesData = ret.selectall_sql(QuesSql)
    res = QuesData
    ret.close()
    return res


def CreateQuest(data):
    sql = "insert into `meta_questionnaire` SET QuesID={},  ProjectID={}, QuesTitle='{}', QuesLeads='{}', Respondents='{}', SurveyType={}, " \
          "SamplePlan='{}', SampleRepresentation='{}', ImplementOrgan='{}',ImplementTime='{}',  DataChannel={}, DataSource='{}'," \
          "QuesStatus={}, CreateTime='{}';".format(
        data["QuesID"], data["ProjectID"],
        data["QuesTitle"], data["QuesLeads"],
        data["Respondents"], data["SurveyType"],
        data["SamplePlan"], data["SampleRepresentation"],
        data["ImplementOrgan"], data["ImplementTime"],
        data["DataChannel"], data["DataSource"],
        data["QuesStatus"], data['CreateTime'])
    ret = MyPymysql('metadata')
    ret.idu_sql(sql)
    ret.close()


def CreateQuestInfo(data):
    # QuestInfoData = {"QuesID": QuesID, "InfoTile": InfoTile, "InfoContent": InfoContent, "EditUserID": EditUserID,
    #                  "EditTime": EditTime, "CreateTime": CreateTime}
    sql = "insert into `meta_questionnaire_info` SET QuesID={}, InfoTile='{}', InfoContent='{}', EditUserID={}, CreateTime='{}';".format(
        data["QuesID"], data["InfoTile"], data["InfoContent"], data["EditUserID"], data["CreateTime"])

    ret = MyPymysql('metadata')
    ret.idu_sql(sql)
    ret.close()


def CreateQuestFile(data):
    # data = {"QuesID": QuesID, "FileTile": FileTile, "FileDescript": FileDescript, "FileType": FileType,
    #              "FilePath": FilePath, "FilePublic": FilePublic, "AuthorUserIDs": AuthorUserIDs,
    #              "UploadUserID": UploadUserID,
    #              "UploadTime": UploadTime, "FileMD5": FileMD5, "FileStatus": FileStatus, "EditTime": EditTime}
    sql = "insert into `meta_questionnaire_files` SET QuesID={}, FileTile='{}', FileDescript='{}', FileType='{}',FilePath='{}', " \
          "FilePublic={},  AuthorUserIDs='{}',UploadUserID={}, UploadTime='{}', FileMD5='{}', FileStatus={}".format(
        data["QuesID"], data["FileTile"],
        data["FileDescript"], data["FileType"],
        data["FilePath"], data["FilePublic"],
        data["AuthorUserIDs"], data["UploadUserID"],
        data["UploadTime"], data["FileMD5"],
        data["FileStatus"])

    ret = MyPymysql('metadata')
    ret.idu_sql(sql)
    ret.close()



def CreateQuestUsers(data):
    # data = {"QuesID": QuesID, "UserID": UserID, "UserRole": UserRole, "UserPrivilege": UserPrivilege,
    #              "UserStatus": UserStatus, "CreateTime": CreateTime}

    sql = "insert into `meta_questionnaire_users` SET QuesID={}, UserID={}, UserRole={}, UserPrivilege='{}', UserStatus={}, CreateTime='{}'".format(
        data["QuesID"], data["UserID"], data["UserRole"], data["UserPrivilege"], data["UserStatus"], data["CreateTime"]
    )
    ret = MyPymysql('metadata')
    ret.idu_sql(sql)
    ret.close()

def SelectAllVable(QuesID):
    try:
        ret = MyPymysql('metadata')
        DataTableIDSql = "select DataTableID from `meta_data_table` WHERE QuesID='{}';".format(QuesID)

        DataTableID = ret.selectall_sql(DataTableIDSql)
        print(DataTableID)
        if DataTableID:
            DataTableID = DataTableID[0]["DataTableID"]
        sql = "select VariableID, DataTableID, OrderNum, VarName, VarTopic, VarLabel from `meta_variable` WHERE DataTableID='{}';".format(DataTableID)
        print(sql)
        alldata = ret.selectall_sql(sql)
        print(alldata)
        ret.close()
    except Exception as e:
        my_log.error(e)
        alldata = 5002
    return alldata

def SelectSbuVable(data):

    sql = "select VariableID, DataTableID, OrderNum, NarName from `meta_variable` WHERE DataTableID='{}';".format(data)
    ret = MyPymysql('metadata')
    alldata = ret.selectall_sql(sql)
    ret.close()
    return alldata



if __name__ == '__main__':
    import re

    # data = ('121212', '12121212', 'aaa', 'aa', 'aa', 1, 1, 1, 1, '11', 1, 111.0, '111', 1, 1, '111', '2012-10-10')
    # CreateMetaProj(data)
    # ret = re.search(r"[\/|\\].*[\/|\\]", SelectProFile(12)[0]["FilePath"]).group()
    # print(ret)

    ret = SelectSbuProInfor('2017051820030259328348437454')
    print(ret)
