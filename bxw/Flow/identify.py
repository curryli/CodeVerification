#coding:utf-8
import cv2
import cv2.cv as cv
from PIL import Image,ImageDraw
import os
import numpy as np
import os.path

#二值数组
t2val = {}
def twoValue(image,G):
    for y in xrange(0,image.size[1]):
        for x in xrange(0,image.size[0]):
            g = image.getpixel((x,y))
            if g > G:
                t2val[(x,y)] = 1
            else:
                t2val[(x,y)] = 0
 
# 降噪 
# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点 
# G: Integer 图像二值化阀值 
# N: Integer 降噪率 0 <N <8 
# Z: Integer 降噪次数 
# 输出 
#  0：降噪成功 
#  1：降噪失败 
def clearNoise(image,N,Z):
 
    for i in xrange(0,Z):
        t2val[(0,0)] = 1
        t2val[(image.size[0] - 1,image.size[1] - 1)] = 1
 
        for x in xrange(1,image.size[0] - 1):
            for y in xrange(1,image.size[1] - 1):
                nearDots = 0
                L = t2val[(x,y)]
                if L == t2val[(x - 1,y - 1)]:
                    nearDots += 1
                if L == t2val[(x - 1,y)]:
                    nearDots += 1
                if L == t2val[(x- 1,y + 1)]:
                    nearDots += 1
                if L == t2val[(x,y - 1)]:
                    nearDots += 1
                if L == t2val[(x,y + 1)]:
                    nearDots += 1
                if L == t2val[(x + 1,y - 1)]:
                    nearDots += 1
                if L == t2val[(x + 1,y)]:
                    nearDots += 1
                if L == t2val[(x + 1,y + 1)]:
                    nearDots += 1
 
                if nearDots < N:
                    t2val[(x,y)] = 1
 
def saveImage(filename,size):
    image = Image.new("1",size)
    draw = ImageDraw.Draw(image)
 
    for x in xrange(0,size[0]):
        for y in xrange(0,size[1]):
            draw.point((x,y),t2val[(x,y)])
 
    image.save(filename)



def getCutList(ffile):
    greyImgList = []
    
    img=cv.LoadImage(ffile)
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
            twoValue(greyImg,100)
            clearNoise(greyImg,2,1)
            greyImgList.append(greyImg)

    return greyImgList


def getmax(imgfile):
    compare_dict = {} 
    img_to_compare = np.asarray(imgfile)

    #rootdir = r"full"
    rootdir = r"D:\verify\bxw\full"
    filelist = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(filelist)):
        path = os.path.join(rootdir,filelist[i])
        if os.path.isfile(path):
            #print path     
            template = cv2.imread(path,0)   
            meth = 'cv2.TM_CCOEFF_NORMED'
            method = eval(meth)
            res = cv2.matchTemplate(img_to_compare,template,method)
            #print res[0][0]
            compare_dict[res[0][0]] = path

    maxFlag = ""
    maxSim = max(compare_dict.keys())
    #print maxSim, compare_dict[maxSim]
    simNum = int(compare_dict[maxSim].split("\\")[-1][0])
    return [simNum,maxSim]
    
if __name__ == '__main__':
    ffile = r"D:\verify\bxw\bxw5.png"
    img = Image.open(ffile)
    imgSize = img.size
    dwidth = imgSize[0]/6
    dheight = imgSize[1]/6

    greyImgList = getCutList(ffile)
#    print greyImgList

    infoDict = {}
    tempPropList = []
    for i in range(0,len(greyImgList)):
        img = greyImgList[i]
        prop = [i,getmax(img)[1]]
        simNum = getmax(img)[0]
        if(infoDict.has_key(simNum)):
            if(prop[1]>infoDict[simNum][1]):
                tempPropList.append(infoDict[simNum])
                infoDict[simNum]= prop
            else:
                tempPropList.append(prop)
        else:
            infoDict[simNum]= prop

    nokey_list = [item for item in infoDict.keys() if item not in range(1,10)]

##    print tempPropList
##    print infoDict.keys()
##    print nokey_list
    for k in range(0,len(nokey_list)):
        infoDict[nokey_list[k]] = tempPropList[k]
        
    print infoDict
    
    givenList = [2,4,1,7]
    for i in givenList:
        x =  infoDict[i][0]/3
        y = infoDict[i][0]%3
   
        print i, [dwidth*(x*2+1), dheight*(y*2+1)]
    

        
        


 
            
        
        


