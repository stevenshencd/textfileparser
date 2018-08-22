#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from __future__ import print_function
#
# """
# This is a general class to provide functions for text file analysis and report.
# """
import csv
import time


class TextParser(object):
    def __init__(self):
        print("csv parsering started")

    @staticmethod
    def opencsvfile(filename):
        print("open CSV file")
        return csv.reader(open(filename, "r"))

    @staticmethod
    def output(filename):
        return open(filename, "a")

    def sum_by_itag(self, inputpath):
        itags = []  # list of execution status by I-Tag
        record = {"ITag": "", "Stage": "", "Pass": 0, "Failed": 0, "NoRun": 0, "Blocked": 0, "NA": 0,
                  "NotComplete": 0, "Others": 0}

        csvdata = self.opencsvfile(inputpath)

        for i, row in enumerate(csvdata):
            # to add function for different parser and report, and to replace following lines
            if i > 0:  # first row is head line, looping start from second row
                if len(itags) == 0:  # for vacant itags list
                    record["ITag"] = row[1]
                    record["Stage"] = row[2]
                    status = row[3]
                    if status == "Passed":
                        record["Pass"] = 1
                    elif status == "Failed":
                        record["Failed"] = 1
                    elif status == "No Run":
                        record["NoRun"] = 1
                    elif status == "Blocked":
                        record["Blocked"] = 1
                    elif status == "Not Completed":
                        record["NotComplete"] = 1
                    elif status == "N/A":
                        record["NA"] = 1
                    else:
                        record["Others"] = 1
                    itags.append(record)
                else:
                    itag_existed = 0
                    for r in itags:
                        if r["ITag"] == row[1] and r["Stage"] == row[2]:
                            itag_existed = 1
                            status = row[3]
                            if status == "Passed":
                                r["Pass"] = int(r["Pass"]) + 1
                            elif status == "Failed":
                                r["Failed"] = int(r["Failed"]) + 1
                            elif status == "No Run":
                                r["NoRun"] = int(r["NoRun"]) + 1
                            elif status == "Blocked":
                                r["Blocked"] = int(r["Blocked"]) + 1
                            elif status == "Not Completed":
                                r["NotComplete"] = int(r["NotComplete"]) + 1
                            elif status == "N/A":
                                r["NA"] = int(r["NA"]) + 1
                            else:
                                r["Others"] = int(r["Others"]) + 1

                    if itag_existed == 0:
                        new_itag = {"ITag": row[1], "Stage": row[2], "Pass": 0, "Failed": 0, "NoRun": 0, "Blocked": 0,
                                    "NA": 0, "NotComplete": 0, "Others": 0}
                        status = row[3]
                        if status == "Passed":
                            new_itag["Pass"] = 1
                        elif status == "Failed":
                            new_itag["Failed"] = 1
                        elif status == "No Run":
                            new_itag["NoRun"] = 1
                        elif status == "Blocked":
                            new_itag["Blocked"] = 1
                        elif status == "Not Completed":
                            new_itag["NotComplete"] = 1
                        elif status == "N/A":
                            new_itag["NA"] = 1
                        else:
                            new_itag["Others"] = 1

                        itags.append(new_itag)
        # sort values by itag
        itags.sort(key= lambda dic: dic["ITag"]+dic["Stage"])
        # write result to file
        reportdate = str(time.strftime("%Y-%m-%d", time.localtime()))
        fout = self.output("ITagreport_" + reportdate + ".csv")
        headline = "Date,ITag,Stage,Pass,Failed,Blocked,NoRun,NotComplete,NA,Others\n"
        fout.write(headline)
        for item in itags:
            line = reportdate + "," + item["ITag"] + "," + item["Stage"] + "," + str(item["Pass"]) + "," + str(
                item["Failed"]) + "," +\
                str(item["Blocked"]) + "," + str(item["NoRun"]) + "," + str(item["NotComplete"]) +\
                "," + str(item["NA"]) + "," + str(item["Others"]) + "\n"
            fout.write(line)
        fout.close()
        print("summing by ITag is successful")

    def sum_by_stage(self, inputpath):
        stages = []  # list of execution status by I-Tag
        record = {"Stage": "", "Pass": 0, "Failed": 0, "NoRun": 0, "Blocked": 0, "NA": 0, "NotComplete": 0,
                  "Others": 0}
        csvdata = self.opencsvfile(inputpath)
        for i, row in enumerate(csvdata):
            # to add function for different parser and report, and to replace following lines
            if i > 0:  # first row is head line, looping start from second row
                if len(stages) == 0:  # for vacant stages list
                    record["Stage"] = row[2]
                    status = row[3]
                    if status == "Passed":
                        record["Pass"] = 1
                    elif status == "Failed":
                        record["Failed"] = 1
                    elif status == "No Run":
                        record["NoRun"] = 1
                    elif status == "Blocked":
                        record["Blocked"] = 1
                    elif status == "Not Completed":
                        record["NotComplete"] = 1
                    elif status == "N/A":
                        record["NA"] = 1
                    else:
                        record["Others"] = 1

                    stages.append(record)
                else:
                    stageexisted = 0
                    for r in stages:
                        if r["Stage"] == row[2]:
                            stageexisted = 1
                            status = row[3]
                            if status == "Passed":
                                r["Pass"] = int(r["Pass"]) + 1
                            elif status == "Failed":
                                r["Failed"] = int(r["Failed"]) + 1
                            elif status == "No Run":
                                r["NoRun"] = int(r["NoRun"]) + 1
                            elif status == "Blocked":
                                r["Blocked"] = int(r["Blocked"]) + 1
                            elif status == "Not Completed":
                                r["NotComplete"] = int(r["NotComplete"]) + 1
                            elif status == "N/A":
                                r["NA"] = int(r["NA"]) + 1
                            else:
                                r["Others"] = int(r["Others"]) + 1

                    if stageexisted == 0:
                        new_stage = {"Stage": row[2], "Pass": 0, "Failed": 0, "NoRun": 0, "Blocked": 0, "NA": 0,
                                     "NotComplete": 0, "Others": 0}
                        status = row[3]
                        if status == "Passed":
                            new_stage["Pass"] = 1
                        elif status == "Failed":
                            new_stage["Failed"] = 1
                        elif status == "No Run":
                            new_stage["NoRun"] = 1
                        elif status == "Blocked":
                            new_stage["Blocked"] = 1
                        elif status == "Not Completed":
                            new_stage["NotComplete"] = 1
                        elif status == "N/A":
                            new_stage["NA"] = 1
                        else:
                            new_stage["Others"] = 1

                        stages.append(new_stage)
        # sort values by stage
        stages.sort(key=lambda dic: dic["Stage"])
        # write result to file
        reportdate = str(time.strftime("%Y-%m-%d", time.localtime()))
        fout = self.output("Stagereport_" + reportdate + ".csv")

        headline = "Date,Stage,Pass,Failed,Blocked,NoRun,NotComplete,NA,Others\n"
        fout.write(headline)
        for item in stages:
            line = reportdate + "," + item["Stage"] + "," + str(item["Pass"]) + "," + str(item["Failed"]) + "," +\
                str(item["Blocked"]) + "," + str(item["NoRun"]) + "," + str(item["NotComplete"]) +\
                "," + str(item["NA"]) + "," + str(item["Others"]) + "\n"
            fout.write(line)
        fout.close()
        print("summing  by stage is successful")

if __name__ == '__main__':
    inputpath = "utms_report_20180730-020541.csv"
    TextParser().sum_by_itag(inputpath)
    TextParser().sum_by_stage(inputpath)

