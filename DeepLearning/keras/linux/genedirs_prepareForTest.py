# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:55:03 2017

@author: lxr
"""

import os,sys
base = 'myvaliddata/'
os.mkdir(base)

ss = "0123456789abcdefghijklmnopqrstuvwxyz"
for i in ss:
    file_name = base+i
    os.mkdir(file_name)
    
    
upList = {"A2","B2","C2","D2","E2","F2","G2","H2","I2","J2","K2","L2",
          "M2","N2","O2","P2","Q2","R2","S2","T2","U2","V2","W2","X2",
          "Y2","Z2"}
for j in upList:
    file_name = base+j
    os.mkdir(file_name)