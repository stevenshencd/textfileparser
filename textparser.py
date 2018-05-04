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
        firstline = f.readline()



if __name__ == '__main__':
    textparser().openfile("")