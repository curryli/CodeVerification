# -*- coding: utf-8 -*-

import sys
import os
import cv2
import numpy as np
import subprocess
from PIL import Image,ImageEnhance,ImageFilter


#由于都是数字    
#对于识别成字母的 采用该表进行修正    
rep={'O':'0',    
    'I':'1',
    'L':'1',    
    'Z':'2',    
    'S':'5',
    'Q':'0',
    '}':'1',
    'E':'6',
    ']':'1',
    'B':'8',
     '`':'',
     ',':'',
     '.':'',
     '\\':'',
     '*':''
    };  
    
    
scratch_image_name = "temp.bmp" # This file must be .bmp or other Tesseract-compatible format
scratch_text_name_root = "temp" # Leave out the .txt extension
cleanup_scratch_flag = True  # Temporary files cleaned up after OCR operation
tesseract_exe_name = 'tesseract' # Name of executable to be called at command line


def filterByPIL(img_name):
    im = Image.open(img_name + ".jpg")
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    data = im.getdata()
    w,h = im.size
    #im.show()
    black_point = 0
    for x in xrange(1,w-1):
        for y in xrange(1,h-1):
            mid_pixel = data[w*y+x]  
            if mid_pixel == 0: 
                top_pixel = data[w*(y-1)+x]
                left_pixel = data[w*y+(x-1)]
                down_pixel = data[w*(y+1)+x]
                right_pixel = data[w*y+(x+1)]
 
                if top_pixel == 0:
                    black_point += 1
                if left_pixel == 0:
                    black_point += 1
                if down_pixel == 0:
                    black_point += 1
                if right_pixel == 0:
                    black_point += 1
                if black_point >= 3:
                    im.putpixel((x,y),0)
                #print black_point
                black_point = 0
    
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(8)
    #im = im.convert('1')
    im.save(img_name + "_t1.jpg")
    
def filterByCV2(img_name):
    img = cv2.imread(img_name + ".jpg", 0)    # 读取参数作为文件名
    adaptive = cv2.adaptiveThreshold(img, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)   # 自适应二值化
    
    adaptive = cv2.medianBlur(adaptive,1) 
    adaptive = adaptive[4:-4, 7:-7]     # 去掉周围的一点点边界

    k = 1
    adaptive = cv2.blur(adaptive, (k,k))
    #adaptive = cv2.GaussianBlur(adaptive, (k,k), 3) 
    cv2.imwrite(img_name + "_t2.jpg", adaptive)   # 存起来

    
def call_tesseract(input_filename, output_filename):
    args = [tesseract_exe_name, input_filename, output_filename]
    proc = subprocess.Popen(args)
    retcode = proc.wait()
  
def retrieve_text(scratch_text_name_root):
    inf = file(scratch_text_name_root + '.txt')
    text = inf.read()
    inf.close()
    return text

def getverify1(name):          
    #打开图片    
    im = Image.open(name)    
    call_tesseract(name, scratch_text_name_root)
    text = retrieve_text(scratch_text_name_root)
    #print text  
    #识别对吗    
    text = text.strip()    
    text = text.upper();      
    for r in rep:    
        text = text.replace(r,rep[r])     
    #out.save(text+'.jpg')    
    #print text    
    return text
    
if __name__=='__main__':
    img_name = "9"
    filterByPIL(img_name)
    result = getverify1(img_name + "_t1.jpg")
    os.remove(img_name + "_t1.jpg")
    if(result==''):
        filterByCV2(img_name)
        result = getverify1(img_name + "_t2.jpg")
        os.remove(img_name + "_t2.jpg")
    print result