#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a general clase to provide functions for text file ready, analysis and report.
"""
import os
import shutil

class textparser:

    def __init__(self):
        print "init"

    def openfile(self,filename):
        return open(filename,"r")

    def output(self,filename):
        return open(filename, "w")

    def criticalIssue(self):
        print "function"
    def getfilebox(self):
        print "open window"

#end of class