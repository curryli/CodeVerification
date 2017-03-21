# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:55:03 2017

@author: lxr
"""

import os,sys
base = 'outImgs_test/'
os.mkdir(base)

ss = "0123456789abcdefghijklmnopqrstuvwxyz"
for i in ss:
    file_name = base+i
    os.mkdir(file_name)