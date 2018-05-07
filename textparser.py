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

    def output(self,filename):
        if filename == '' :
            filename = tkFileDialog.askopenfilename(initialdir='C:/')
        return open(filename, "w")

    def csvparser(self):
        f = self.openfile("")
        reader = csv.reader(f)
        totalpass = 0
        for i, rows in enumerate(reader):
            # to add function for different parser and report, and to replace following lines
            if i >0:
                totalpass = totalpass + int(rows[1])

        print "total pass:", totalpass

if __name__ == '__main__':
    textparser().csvparser()