# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:55:03 2017

@author: lxr
"""

import os,sys
base = 'createdImgs'
#os.mkdir(base)


for i in range(11,40):
    file_name = base+str(i) + '/'
    os.mkdir(file_name)