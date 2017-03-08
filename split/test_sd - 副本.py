# -*- coding: utf-8 -*-
# 验证码识别，此程序只能识别数据验证码  
from PIL import Image,ImageEnhance,ImageFilter
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
sys.path.append('pytesser/') 

#from pytesser import *  
# 二值化    
threshold = 140    
table = []    
for i in range(256):    
    if i < threshold:    
        table.append(0)    
    else:    
        table.append(1)    
 
#由于都是数字    
#对于识别成字母的 采用该表进行修正    
rep={'O':'0',    
    'I':'1','L':'1',    
    'Z':'2',    
    'S':'8'    
    };    
 
def  getverify1(name):          
    #打开图片    
    #im = Image.open(name)    
   
    #text = image_to_string(im)    
    #识别对吗    
    #text = text.strip()    
    #text = text.upper()
    print "Done1"
    #for r in rep:    
    #    text = text.replace(r,rep[r])     
    #out.save(text+'.jpg')    
    #print text
    
    #return text

if __name__ == '__main__':
    #getverify1('sd1_new.jpg')  #注意这里的图片要和此文件在同一个目录，要不就传绝对路径也行
    print "Done2"
