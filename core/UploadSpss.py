#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import savReaderWriter
import os
import datetime, time
import uuid
from common.base import my_log
from common.base import Config, MyPymysql
from models.UploadSpssModel import create_data_table, writer_data_table
from models.UploadSpssModel import create_information_tables, writer_information_tables, CreateDataTableInfor
from common.base import MyGuid



class upload_spss():

    def __init__(self):
        self.vartypes = []  # ['A20', 'F8.2', 'F8', 'DATETIME20'] spss类型
        self.width = []  # ['20', '8.2', '8', '20'] 宽度
        self.valuetypes = []  # 数据类型
        self.float_width = []

    def read_sav(self, filepath):

        with savReaderWriter.SavReader(filepath, ioUtf8=True) as read:
            ret = read.getSavFileInfo()
            # return (self.numVars, self.nCases, self.varNames, self.varTypes,
            #         self.formats, self.varLabels, self.valueLabels)
            print(ret[0])
            # return read.formats, read.varNames, read.varLabels, read.valueLabels
            return ret[4], ret[2], ret[5], ret[6]

    def get_spss_data(self, formats, varnames):
        for i in varnames:
            self.vartypes.append(formats[i])
            if formats[i].startswith("F"):
                ret = formats[i].split("F")[1]
                self.width.append(ret)
                ret1 = ret.split(".")
                if ret1[1:]:
                    self.valuetypes.append("FLOAT")
                else:
                    self.valuetypes.append("INT")

            elif formats[i].startswith("A"):
                ret = formats[i].split("A")[1]
                self.width.append(ret)
                self.valuetypes.append("VARCHAR")

            elif formats[i].startswith("DATE"):
                if formats[i].split("DATE")[1].startswith("TIME"):
                    ret = formats[i].split("DATETIME")[1]
                    self.width.append(ret)
                    self.valuetypes.append("DATETIME")
                else:
                    ret = formats[i].split("DATE")[1]
                    self.width.append(ret)
                    self.valuetypes.append("DATE")
        return self.vartypes, self.width, self.valuetypes

    def float_data(self, width):

        for i in width:
            if i.split(".")[1:]:
                dec = i.split(".")
                self.float_width.append(dec[1])
            else:
                self.float_width.append(0)
        return self.float_width

    def writer_data(self, filepath, filename, valuetypes, tablename):
        res = writer_data_table()
        with savReaderWriter.SavReader(filepath, ioUtf8=True) as read:
            # 如果不用ioutf8， 汉字十六进制\被转义，更麻烦
            try:
                for i in read:
                    for j in range(len(valuetypes)):
                        # 数据库不认unicode所以要转换下
                        # 将varchar进行json存如数据库
                        if valuetypes[j] == "DATETIME":
                            i[j] = read.spss2strDate(i[j], '%Y-%m-%d %H:%M:%S', None)
                        elif valuetypes[j] == "DATE":
                            i[j] = read.spss2strDate(i[j], '%Y-%m-%d', None)
                        elif valuetypes[j] == "VARCHAR":
                            i[j] = i[j]
                    res.insert_sql(tablename, i)
            except Exception as e:
                my_log.error(e)
            finally:
                my_log.info("data write database success !!!")
        res.close()

    def writer_moredata(self, filepath, filename, valuetypes, start, end, tablename):
        res = writer_data_table()
        with savReaderWriter.SavReader(filepath, ioUtf8=True) as read:
            # 如果不用ioutf8， 汉字十六进制\被转义，更麻烦
            try:
                for i in read:
                    i = i[start:end]
                    for j in range(len(valuetypes)):
                        # 数据库不认unicode所以要转换下
                        # 将varchar进行json存如数据库
                        if valuetypes[j] == "DATETIME":
                            i[j] = read.spss2strDate(i[j], '%Y-%m-%d %H:%M:%S', None)
                        elif valuetypes[j] == "DATE":
                            i[j] = read.spss2strDate(i[j], '%Y-%m-%d', None)
                        elif valuetypes[j] == "VARCHAR":
                            i[j] = i[j]
                    res.insert_sql(tablename, i)
            except Exception as e:
                my_log.error(e)
            finally:
                my_log.info("data write database success !!!")
        res.close()

    # def insert_sub_table(self, filename, varnames, valuetypes, width, float_width,varLabels, valueLabels, vartypes,project_id,dataset_id):
    def insert_sub_table(self, DataTableID, varnames, my_valuetypes, my_width, float_width, varLabels, valueLabels, my_vartypes):
        # print(my_width)
        try:
            res = writer_information_tables()
            for i in range(len(varnames)):
                data = {}
                data["DataTableID"] = DataTableID
                data["OrderNum"] = i
                data["VarName"] = varnames[i]
                data["VarType"] = my_valuetypes[i]
                if self.width[i]:
                    data["VarWidth"] = self.width[i]
                else:
                    data["VarWidth"] = 20
                data["VarDecimals"] = float_width[i]
                data["OriginFormats"] = my_vartypes[i]
                data["VarMeasure"] = 0
                # data.append(varLabels[varnames[i]].replace('\u3000', ' '))  # 注意这里: 存之前: Ｆ1.0　请根据你的实际情况，  存之后:Ｆ4.0u3000请根据你的实际情况，在下列描述中，选择符合你的程度，并选择
                if varnames[i] in valueLabels:
                    json_unicode_dict = json.dumps(valueLabels[varnames[i]], ensure_ascii=False)
                    data["VarValues"] = json_unicode_dict
                else:
                    data["VarValues"] = 0
                data["VarMissing"] = "Null"
                data["VarTopic"] = "Null"
                data["VarLabel"] = varLabels[varnames[i]].replace('\u3000', ' ')
                data["OriginQuestion"] = "Null"
                data["OtherLangLabel"] = "Null"
                data["DataFrom"] = "Null"
                data["DeriveFrom"] = "Null"
                data["VarRole"] = "Null"
                data["VarVersion"] = 1
                data["ReviseFrom"] = "Null"
                data["ReviseTime"] = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                data["ReviseUserID"] = "Null"
                data["VarNote"] = "Null"
                data["VarStatus"] = 1
                # sql = res.insert_sql(filename, data)
                res.insert_sql(data)
            res.close()
        except Exception as e:
            my_log.error(e)
            return

        my_log.info("write spss data head information successful!")

    def main(self, FilePath, filename, user_id, QuesID):
        """
        # print(formats):{'Q8': 'A400', 'Q3R6': 'F5', 'Q5R3': 'F5', }
        # print(varnames)['ID', 'StartTime', 'EndTime', 'VerNo', 'Q1R3',]
        # print(varLabels){'Q8': 'Q2. 学号', 'Q3R6': 'Ｆ2.2\u3000请根据你的实际情况，
        # print(valueLabels){'Q3R6': {1.0: '非常不符合', 2.0: '比较不符合',
        # print("vartypes", my_vartypes) ['A20', 'DATETIME40', 'DATETIME40',
        # print(width) ['20', '40', '40', '5', '5', '5', '5',
        # print(my_valuetypes) ['VARCHAR', 'DATETIME', 'DATETIME', 'INT',
        # print(float_width)[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        """

        # filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "file", filename)
        FilePathName = FilePath
        # 得到文件信息
        formats, varnames, varLabels, valueLabels = self.read_sav(FilePathName)
        my_vartypes, my_width, my_valuetypes = self.get_spss_data(formats, varnames)
        float_width = self.float_data(self.width)
        for i in range(len(my_vartypes)):
            if my_vartypes[i].startswith("F"):
                if my_vartypes[i].split(".")[1:]:
                    pass
                else:
                    my_vartypes[i] = my_vartypes[i] + ".0"

        # 创建表
        # 不允许超过1024列MySQL, 超过了分表
        DataTableID = MyGuid()
        tablename = "db"+DataTableID

        DataTableStatus = 1
        if len(varnames) < 1024:
            num = 1
            # table_subname = "u" + str(user_id) + "_" + str(nowtime) + "_" + str(new_time3) + "_" + str(num)
            table_subname = tablename + "_" + str(num)
            try:
                create_data_table(my_vartypes, my_width, my_valuetypes, formats, varnames, table_subname)
                self.writer_data(FilePath, filename, my_valuetypes, table_subname)
                ConfInfo = Config().get_content("data")
                DataTableInfo = {"DataTableID": DataTableID, "QuesID":QuesID, "DataServerIP": ConfInfo["host"],
                                 "DataServerPort": ConfInfo["port"], "DatabaseName": ConfInfo["db_name"],
                                 "DataTableName": table_subname, "DataTableStatus": DataTableStatus}
                CreateDataTableInfor(DataTableInfo)

            except Exception as e:
                my_log.error(e)
        else:
            try:
                integer, remainder = divmod(len(varnames), 800)
                if remainder:
                    integer += 1
                for num in range(1, integer + 1):
                    # table_subname = filename + "_" + str(num)
                    # table_subname = "u" + str(user_id) + "_" + str(nowtime) + "_" + str(new_time3) + "_" + str(num)
                    table_subname = tablename + "_" + str(num)
                    start = num * 800 - 800
                    end = num * 800
                    sub_formats = {}
                    for sub_for in varnames[start:end]:
                        sub_formats[sub_for] = formats[sub_for]

                    create_data_table(my_vartypes[start:end],
                                      my_width[start:end],
                                      my_valuetypes[start:end],
                                      sub_formats,  # formats
                                      varnames[start:end],
                                      table_subname)
                    self.writer_moredata(FilePath, filename, my_valuetypes[start:end], start, end, table_subname)
                    ConfInfo = Config().get_content("data")
                    DataTableInfo = {"DataTableID": DataTableID, "QuesID": QuesID, "DataServerIP": ConfInfo["host"],
                                     "DataServerPort": ConfInfo["port"], "DatabaseName": ConfInfo["db_name"],
                                     "DataTableName": table_subname, "DataTableStatus": DataTableStatus}
                    CreateDataTableInfor(DataTableInfo)
            except Exception as e:
                my_log.error(e)



        # 信息表值创建一个
        # create_information_tables(filename)
        # 写入数据(标签等信息)
        # self.insert_sub_table(DataTableID, varnames, my_valuetypes, my_width, float_width, varLabels, valueLabels,my_vartypes)
        try:
            # self.insert_sub_table(filename, varnames, my_valuetypes, my_width, float_width, varLabels, valueLabels,
            #                  my_vartypes,project_id, dataset_id)
            self.insert_sub_table(DataTableID, varnames, my_valuetypes, my_width, float_width, varLabels, valueLabels, my_vartypes)
        except Exception as e:
            my_log.error(e)

        return DataTableID


if __name__ == '__main__':
    filename = "1111.sav"
    # main(filename)
