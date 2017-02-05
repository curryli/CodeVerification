import cv2
import numpy as np
import os
import os.path

 


compare_dict = {} 
img_to_compare = cv2.imread('material\\bxw5_5.png',0)

#rootdir = r"full"
rootdir = r"allTemp"
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
print maxSim, compare_dict[maxSim]


##for k in compare_dict.keys():
##    print k, compare_dict[k]
    
        
