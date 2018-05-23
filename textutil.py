#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
libraries for text line processing
"""

# return a list
def seperate(line, seperator):
    return line.split(seperator)


def demo():
    print 'using coma for multi value:', 'print x, y, z'
    values = [1, 2, 3, 4, 5, 6]
    if len(values)> 3:
        print values[0:2]
    for val in values:
        print val
    i = 0
    while i < 6:
        print values[i]
        i+=1
        if i == 2:
            break
    d = {'name':'ss', 'age':28}
    print d['age'], d['name'], d.viewvalues()

demo()