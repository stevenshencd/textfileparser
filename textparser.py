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
        return open(filename, "w")

    def inquery_pass(self):
        csvdata = self.opencsvfile("")
        totalpass = 0
        for i, row in enumerate(csvdata):
            # to add function for different parser and report, and to replace following lines
            if i > 0:
                totalpass = totalpass + int(row[1])

        fout = self.output("")
        fout.write("total pass:" + str(totalpass))
        fout.close()

if __name__ == '__main__':
    textparser().inquery_pass()
