#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import datetime
from common.base import Config, MyPymysql
from common.base import my_log



# 写入数据表信息
def CreateDataTableInfor(data):
    # DataTableInfo = {"DataTableID": DataTableID, "QuesID": QuesID, "DataServerIP": ConfInfo["host"],
    #                  "DataServerPort": ConfInfo["port"], "DatabaseName": ConfInfo["db_name"],
    #                  "DataTableName": table_subname, "DataTableStatus": DataTableStatus}
    sql = "insert into `meta_data_table` SET DataTableID='{}', QuesID={}, DataServerIP='{}',DataServerPort={}, DatabaseName='{}', " \
          "DataTableName='{}', DataTableStatus={};".format(
        data["DataTableID"], data["QuesID"],
        data["DataServerIP"],data["DataServerPort"],
        data["DatabaseName"],data["DataTableName"], data["DataTableStatus"])
    ret = MyPymysql('metadata')
    ret.idu_sql(sql)
    ret.close()

# 创建数据表
def create_data_table(vartypes, width, valuetypes, formats, varnames, tablename, libname="data"):

    sql = """CREATE TABLE `{}` (""".format(tablename)
    for i in range(len(varnames)):
        if valuetypes[i] == "FLOAT":
            num = width[i].split(".")
            s = "`{}` {}({},{}) DEFAULT NULL".format(varnames[i], valuetypes[i], num[0], num[1])
        elif valuetypes[i] == "DATETIME":
            s = "`{}` {} DEFAULT NULL".format(varnames[i], valuetypes[i])
        elif valuetypes[i] == "DATE":
            s = "`{}` {} DEFAULT NULL".format(varnames[i], valuetypes[i])
        elif valuetypes[i] == "VARCHAR":
            s = "`{}` {}({}) DEFAULT NULL".format(varnames[i], valuetypes[i], width[i])
        else:
            s = "`{}` {}({}) DEFAULT NULL".format(varnames[i], valuetypes[i], width[i])

        if i < len(varnames) - 1:
            sql = sql + s + ","
        elif i == len(varnames) - 1:
            sql = sql + s

    sql = sql + ") ENGINE=InnoDB DEFAULT CHARSET=UTF8"



    ret = MyPymysql('data')
    ret.idu_sql("""DROP TABLE IF EXISTS {}""".format(tablename))
    ret.idu_sql(sql)
    ret.close()


class writer_data_table():
    def __init__(self, libname="data"):
        self.libname= libname
        self.res = MyPymysql('data')

    def insert_sql(self, tablename, data):
        data = tuple(data)
        sql = """insert INTO `{}` VALUES {};""".format(tablename, data)
        self.res.idu_sql(sql)

    def close(self):
        self.res.close()


def create_information_tables(tablename, libname="information"):
    sql = """CREATE TABLE `{}` (
            `name` VARCHAR (255) DEFAULT NULL,
            `type` VARCHAR (255) DEFAULT NULL,
            `width` INT (5) DEFAULT NULL,
            `float_width` INT (5) DEFAULT NULL,
            `varlabels` text DEFAULT NULL,
            `valuelabels` text DEFAULT NULL,
            `formats` VARCHAR(255) DEFAULT NULL,
            `missing_value` VARCHAR(255) DEFAULT NULL,
            `theme` VARCHAR(255) DEFAULT NULL
            ) ENGINE = INNODB DEFAULT CHARSET = utf8;""".format(tablename)
    res = base_model(libname).connect()
    res.adu_sql(sql)
    res.close()


class writer_information_tables():
    def __init__(self, libname="metadata"):
        self.libname= libname
        self.res = MyPymysql('metadata')

    def insert_sql(self, data):
        sql = "insert INTO `meta_variable` SET DataTableID={}, OrderNum={}, VarName='{}', VarType='{}', " \
              "VarWidth={}, VarDecimals='{}', OriginFormats='{}', VarMeasure={}, VarValues='{}', VarMissing='{}', " \
              "VarTopic='{}', VarLabel='{}', OriginQuestion='{}', OtherLangLabel='{}', DataFrom={}, DeriveFrom='{}', " \
              "VarRole={}, VarVersion={}, ReviseFrom={}, ReviseTime='{}', ReviseUserID={}, VarNote='{}', VarStatus={};".format(
            data["DataTableID"], data["OrderNum"],
            data["VarName"], data["VarType"],
            data["VarWidth"], data["VarDecimals"],
            data["OriginFormats"], data["VarMeasure"],
            data["VarValues"], data["VarMissing"],
            data["VarTopic"],data["VarLabel"],
            data["OriginQuestion"], data["OtherLangLabel"],
            data["DataFrom"], data["DeriveFrom"],
            data["VarRole"], data["VarVersion"],
            data["ReviseFrom"], data["ReviseTime"],
            data["ReviseUserID"], data["VarNote"], data["VarStatus"])
        self.res.idu_sql(sql)

    def close(self):
        self.res.close()


