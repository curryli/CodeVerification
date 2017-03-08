#!/usr/bin/env python
# coding=utf-8
import cv2
import sys
import os

if __name__ == '__main__':

    img = cv2.imread('sc4_new.jpg', 0)    # 读取参数作为文件名
    adaptive = cv2.adaptiveThreshold(img, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)   # 自适应二值化
    
    adaptive = cv2.medianBlur(adaptive,1) 
    adaptive = adaptive[4:-4, 7:-7]     # 去掉周围的一点点边界

    k = 1
    adaptive = cv2.blur(adaptive, (k,k))
    #adaptive = cv2.GaussianBlur(adaptive, (k,k), 3) 

    cv2.imwrite('sc4_new_new.jpg', adaptive)   # 存起来
