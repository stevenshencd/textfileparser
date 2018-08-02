#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a general class to provide functions for text file analysis and report.
"""
import os
import shutil
from Tkinter import *
import tkFileDialog
import csv
import time

class textparser:

    def __init__(self):
        print "csv parsering started"

    def openfile(self,filename):
        if filename == '' :
            filename = tkFileDialog.askopenfilename(initialdir='C:/')
        return open(filename,"r")

    def opencsvfile(self,filename):
        if filename == '' :
            filename = tkFileDialog.askopenfilename(initialdir='C:/')
        return csv.reader(open(filename,"r"))

    def output(self,filename):
        if filename == '' :
            filename = tkFileDialog.asksaveasfilename()
        return open(filename, "a")

    def inquery_pass(self):
        csvdata = self.opencsvfile("")
        totalpass = 0
        for i, row in enumerate(csvdata):
            # to add function for different parser and report, and to replace following lines
            if i>0 :
                totalpass = totalpass + int(row[1])

        fout = self.output("")
        fout.write("total pass:" + str(totalpass))
        fout.close()

    def sumbyITag(self, inputpath):
        ITags = [] # list of execution status by I-Tag
        record = {"ITag":"","Stage":"","Pass":0,"Failed":0,"NoRun":0,"Blocked":0,"NA":0,"NotComplete":0,"Others":0}
        csvdata = self.opencsvfile(inputpath)

        for i, row in enumerate(csvdata):
            # to add function for different parser and report, and to replace following lines
            if i > 0: #first row is head line, looping start from second row
                if len(ITags) == 0: # for vacant ITags list
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
                        record["Others"] =1
                    ITags.append(record)
                else:
                    ITagexisted = 0
                    for r in ITags:
                        if r["ITag"] == row[1] and r["Stage"] == row[2]:
                            ITagexisted = 1
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

                    if ITagexisted == 0:
                        newItag = {"ITag":"","Stage":"","Pass":0,"Failed":0,"NoRun":0,"Blocked":0,"NA":0,"NotComplete":0,"Others":0}
                        newItag["ITag"] = row[1]
                        newItag["Stage"] = row[2]
                        status = row[3]
                        if status == "Passed":
                            newItag["Pass"] = 1
                        elif status == "Failed":
                            newItag["Failed"] = 1
                        elif status == "No Run":
                            newItag["NoRun"] = 1
                        elif status == "Blocked":
                            newItag["Blocked"] = 1
                        elif status == "Not Completed":
                            newItag["NotComplete"] = 1
                        elif status == "N/A":
                            newItag["NA"] = 1
                        else:
                            newItag["Others"] = 1

                        ITags.append(newItag)
        # write result to file
        reportdate = str(time.strftime("%Y-%m-%d", time.localtime()))
        fout = self.output("ITagreport_" + reportdate + ".csv")
        headline = "Date,ITag,Stage,Pass,Failed,Blocked,NoRun,NotComplete,NA,Others\n"
        fout.write(headline)
        for item in ITags:
            line = reportdate + "," + item["ITag"] + "," +item["Stage"] + "," + str(item["Pass"]) + "," + str(item["Failed"]) + "," \
                   + str(item["Blocked"]) + "," + str(item["NoRun"]) + "," + str(item["NotComplete"]) \
                   + "," + str(item["NA"]) + "," + str(item["Others"]) + "\n"
            fout.write(line)
        fout.close()
        print "summing by ITag is successful"

    def sumbyStage(self, inputpath):
        stages = []  # list of execution status by I-Tag
        record = {"Stage": "", "Pass": 0, "Failed": 0, "NoRun": 0, "Blocked": 0, "NA": 0, "NotComplete": 0, "Others": 0}
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
                        newStage = {"Stage": "", "Pass": 0, "Failed": 0, "NoRun": 0, "Blocked": 0, "NA": 0, "NotComplete": 0,
                                   "Others": 0}
                        newStage["Stage"] = row[2]
                        status = row[3]
                        if status == "Passed":
                            newStage["Pass"] = 1
                        elif status == "Failed":
                            newStage["Failed"] = 1
                        elif status == "No Run":
                            newStage["NoRun"] = 1
                        elif status == "Blocked":
                            newStage["Blocked"] = 1
                        elif status == "Not Completed":
                            newStage["NotComplete"] = 1
                        elif status == "N/A":
                            newStage["NA"] = 1
                        else:
                            newStage["Others"] = 1

                        stages.append(newStage)
        # write result to file
        reportdate = str(time.strftime("%Y-%m-%d", time.localtime()))
        fout = self.output("Stagereport_"+ reportdate + ".csv")

        headline = "Date,Stage,Pass,Failed,Blocked,NoRun,NotComplete,NA,Others\n"
        fout.write(headline)
        for item in stages:
            line = reportdate + "," + item["Stage"] + "," + str(item["Pass"]) + "," + str(item["Failed"]) + "," \
                   + str(item["Blocked"]) + "," + str(item["NoRun"]) + "," + str(item["NotComplete"]) \
                   + "," + str(item["NA"]) + "," + str(item["Others"]) + "\n"
            fout.write(line)
        fout.close()
        print "summing by stage is successful"

if __name__ == '__main__':
    inputpath = "utms_report_20180730-020541.csv"
    textparser().sumbyITag(inputpath)
    textparser().sumbyStage(inputpath)

