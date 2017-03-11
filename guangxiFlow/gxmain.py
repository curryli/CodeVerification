# -*- coding: utf-8 -*-

import sys
import os
import cv2
import numpy as np
import subprocess
from PIL import Image,ImageEnhance,ImageFilter


#由于都是数字    
#对于识别成字母的 采用该表进行修正    
rep={ 
    '}':'1',
    ']':'1',
     '`':'',
     ',':'',
     "‘":'',
     "'":'',
     '.':'',
     '\\':'',
     '*':'',
     '_':'',
     ';':''
    };  
    
    
scratch_image_name = "temp.bmp" # This file must be .bmp or other Tesseract-compatible format
scratch_text_name_root = "temp" # Leave out the .txt extension
cleanup_scratch_flag = True  # Temporary files cleaned up after OCR operation
tesseract_exe_name = 'tesseract' # Name of executable to be called at command line
 
    
def call_tesseract(input_filename, output_filename):
    args = [tesseract_exe_name, input_filename, output_filename, "digits"]
    proc = subprocess.Popen(args)
    retcode = proc.wait()
  
def retrieve_text(scratch_text_name_root):
    inf = file(scratch_text_name_root + '.txt')
    text = inf.read()
    inf.close()
    return text

def getverify1(name):          
    im = Image.open(name)    
    call_tesseract(name, scratch_text_name_root)
    text = retrieve_text(scratch_text_name_root)
    #print text  
    #识别对吗    
    text = text.strip()    
    for r in rep:    
        text = text.replace(r,rep[r])        
    #out.save(text+'.jpg')    
    #print text    
    return text
    
if __name__=='__main__':
    img_name = "2"
    print getverify1(img_name + ".jpg")
#    filterByPIL(img_name)
#    result1 = getverify1(img_name + "_t1.jpg")
#    print result1