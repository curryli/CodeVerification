#unfinished
import cv2
import numpy as np
from PIL import Image,ImageDraw
import cv2.cv as cv
import os
import os.path

class Util:  
    #定义基本属性  
    ffile = r"D:\verify\bxw\bxw5.png"
    greyImgList = []
    t2val = {}

    
    #定义构造方法  
    def __init__(self,ffile):  
        self.ffile = ffile  


    #二值数组
    def twoValue(image,G):
        for y in xrange(0,image.size[1]):
            for x in xrange(0,image.size[0]):
                g = image.getpixel((x,y))
                if g > G:
                    self.t2val[(x,y)] = 1
                else:
                    self.t2val[(x,y)] = 0
                    
    def getCutList(self):
        img=cv.LoadImage(self.ffile)
        small_width = img.width/3
        small_height = img.height/3
        tempImg=img
        
        
        
        for i in range(0,3):
            for j in range(0,3):
                item = i+j*3
                cv.SetImageROI(tempImg,(i*small_width,j*small_height,small_width,small_height))
                cv.SaveImage("tempImg.png",tempImg)
                adaptive = cv2.imread("tempImg.png", 0)  # =0 Return a grayscale image.
                os.remove("tempImg.png")
                adaptive = adaptive[3:-3, 3:-3]  # 去掉周围的一点点边界
                #自适应二值化
                adaptive = cv2.adaptiveThreshold(adaptive, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 5)
                
                cv2.imwrite("tempImg.png", adaptive)
                greyImg = Image.open("tempImg.png").convert("L")
                self.twoValue(greyImg,100)
                clearNoise(greyImg,2,1)
                self.greyImgList.append(greyImg)

        return self.greyImgList
                
                
              
      
  
util = Util(r"D:\verify\bxw\bxw5.png")
greyImgList = util.getCutList()
print greyImgList
