#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a general class to provide functions for text file analysis and report.
"""
import os
import shutil
from Tkinter import *
import tkFileDialog
from textutil import *
import csv

class textparser:

    def __init__(self):
        print "init"

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
            print i
            if i>0 :
                totalpass = totalpass + int(row[1])

        fout = self.output("")
        fout.write("total pass:" + str(totalpass))
        fout.close()

    def sumbyITag(self):
        ITags = [] # list of execution status by I-Tag
        record = {"ITag":"","Pass":0,"Failed":0,"NoRun":0,"Blocked":0,"NA":0,"NotComplete":0,"Others":0}
        csvdata = self.opencsvfile("c:\github\data\execution180724.csv")
        print len(ITags)
        print record
        for i, row in enumerate(csvdata):
            # to add function for different parser and report, and to replace following lines
            if i > 0: #first row is head line, looping start from second row
                if len(ITags) == 0: # for vacant ITags list
                    record["ITag"] = row[1]
                    status = row[3]
                    if status == "Pass":
                        record["Pass"] = 1
                    elif status == "Failed":
                        record["Failed"] = 1
                    elif status == "No Run":
                        record["NoRun"] = 1
                    elif status == "Blocked":
                        record["Blocked"] = 1
                    elif status == "Not Complete":
                        record["NotComplete"] = 1
                    elif status == "N/A":
                        record["NA"] = 1
                    else:
                        record["Others"] =1
                    print "fisrt line:"
                    print record
                    ITags.append(record)
                else:
                    ITagexisted = 0
                    for r in ITags:
                        if r["ITag"] == row[1]:
                            ITagexisted = 1
                            status = row[3]
                            if status == "Pass":
                                r["Pass"] = int(r["Pass"]) + 1
                            elif status == "Failed":
                                r["Failed"] = int(r["Failed"]) + 1
                            elif status == "No Run":
                                r["NoRun"] = int(r["NoRun"]) + 1
                            elif status == "Blocked":
                                r["Blocked"] = int(r["Blocked"]) + 1
                            elif status == "Not Complete":
                                r["NotComplete"] = int(r["NotComplete"]) + 1
                            elif status == "N/A":
                                r["NA"] = int(r["NA"]) + 1
                            else:
                                r["Others"] = int(r["Others"]) + 1
                            print "find it:"
                            print r
                    if ITagexisted == 0:
                        newItag = {"ITag":"","Pass":0,"Failed":0,"NoRun":0,"Blocked":0,"NA":0,"NotComplete":0,"Others":0}
                        newItag["ITag"] = row[1]
                        status = row[3]
                        if status == "Pass":
                            newItag["Pass"] = 1
                        elif status == "Failed":
                            newItag["Failed"] = 1
                        elif status == "No Run":
                            newItag["NoRun"] = 1
                        elif status == "Blocked":
                            newItag["Blocked"] = 1
                        elif status == "Not Complete":
                            newItag["NotComplete"] = 1
                        elif status == "N/A":
                            newItag["NA"] = 1
                        else:
                            newItag["Others"] = 1
                        print "new Itag:"
                        print newItag
                        ITags.append(newItag)
        # write result to file

        fout = self.output("c:\github\data\ITagsummary.csv")
        for item in ITags:
            line = item["ITag"] + "," + str(item["Pass"]) + "," + str(item["Failed"]) + "," \
                   + str(item["Blocked"]) + "," + str(item["NoRun"]) + "," + str(item["NotComplete"]) \
                   + "," + str(item["NA"]) + "," + str(item["Others"]) + "\n"
            print line
            fout.write(line)
        fout.close()

if __name__ == '__main__':
    textparser().sumbyITag()
