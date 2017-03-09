# -*- coding: utf-8 -*-

import sys
import os
import cv2
import numpy as np
import subprocess
from PIL import Image,ImageEnhance,ImageFilter


# 二值化    
threshold = 150
table = []    
for i in range(256):    
    if i < threshold:    
        table.append(0)    
    else:    
        table.append(1) 
        
#由于都是数字    
#对于识别成字母的 采用该表进行修正    
rep={ 
    '}':'1',
    ']':'1',
     '`':'',
     ',':'',
     ' ':'',
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


def sum_9_region(img, x, y):
    """
    9邻域框,以当前点为中心的田字框,黑点个数
    :param x:
    :param y:
    :return:
    """
    # todo 判断图片的长宽度下限
    cur_pixel = img.getpixel((x, y))  # 当前像素点的值
    width = img.width
    height = img.height

    if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
        return 0

    if y == 0:  # 第一行
        if x == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:  # 右上顶点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 4 - sum
        else:  # 最上非顶点,6邻域
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下顶点
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - sum
        elif x == width - 1:  # 右边非顶点
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - sum
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum
            
            
def filterByPIL(img_name):
    im = Image.open(img_name + ".jpg")
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(5)
    im = im.convert('1')  # 转化为灰度图
    #二值化，采用阈值分割法，threshold为分割点   
    out = im.point(table,'1')  
    #out.show()
    
    imgry = np.asarray(out)
     
    #print  imgry 

    #print out.size    #60, 20
    #print out.getpixel((30, 10))
    #print sum_9_region(out,0,0)

    delList = []
    for x in range(59):
        for y in range(19):
            count = sum_9_region(out,x,y)
            if(count==1 or count==2):
#                print x,y
#                print count
                delList.append((x,y))
                
    for cor in delList:           
        out.putpixel(cor,1)
    
    out = out.filter(ImageFilter.MedianFilter())
   

    out.show()
     
    out.save(img_name + "_t1.jpg")
    
    
def call_tesseract(input_filename, output_filename):
    args = [tesseract_exe_name, input_filename, output_filename, "digits"]     #
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
    text = text.upper();      
    for r in rep:    
        text = text.replace(r,rep[r])        
    #out.save(text+'.jpg')    
    #print text    
    return text
    
if __name__=='__main__':
    img_name = "38"
#    print getverify1(img_name + ".jpg")
    filterByPIL(img_name)
    result1 = getverify1(img_name + "_t1.jpg")
    print result1

#    filterByCV2(img_name + r"_t1")
#    result2 = getverify1(img_name + "_t1_t2.jpg")
#    print result2