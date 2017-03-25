# -*- coding: utf-8 -*-
from PIL import Image,ImageEnhance,ImageFilter
import numpy as np
from scipy.misc import imread
import random, string

def cut_pic(filename, sp_N):  #图片处理（灰度化，二值化，切割图片）
     filepath = filename
     
     im = Image.open(filepath)
     imgSize = im.size #
     print imgSize   #(130, 50)
     imgry = im.convert('L')  #灰度化
     
       
     #imgry.show()
     #二值化
     threshold = 120
     table = []

     for i in range(256):
         if i <threshold:
             table.append(0)
         else:
             table.append(1)
     biPic = imgry.point(table,'1')

     biPic = biPic.filter(ImageFilter.MedianFilter())
     #biPic.show()
     
     bi_w = biPic.width    
     bi_h = biPic.height
      
     data = biPic.getdata()
     data = np.matrix(data,dtype='int32')
     #new_data = np.reshape(data,(width,height))
     imarray = np.reshape(data,(bi_h,bi_w))
     
     
     imarray = 1-imarray
     #print imarray.shape[1]   #列数
     #print reversedImg
      
     #保存要切割的列
     box = (0, 0, bi_w, bi_h)  # left, upper, right, lower 
     out = biPic.crop(box)
     print out.size 
     
     
     out_w = out.width
     out_h = out.height
     
     realcut = []
     for i in range(sp_N+1):
         realcut.append(i*out_w/sp_N)
     
     
     #realcut = [0, out_w/4, out_w/2, 3*out_w/4, out_w]
     print realcut
     #切割图片
     count = []
     for j in range(sp_N):
         count.append(j)

     child_img_list = []
     for i in count:
         col_left = count*out_w/sp_N
         col_right = (count+1)*out_w/sp_N
         
         child_img = out.crop((realcut[i],0,realcut[i+1],out_h))
         child_img_list.append(child_img)
    
     # 返回切割的图片
     return child_img_list
          
def random_str(randomlength=8):
    a = list(string.ascii_letters + string.digits)
    random.shuffle(a)
    return ''.join(a[:randomlength])    
     
if __name__ == '__main__':
    filename = '45.jpg'
    sp_N = 6
    child_img_list = cut_pic(filename, sp_N)
    #child_img_list = cut_pic('sd1.jpg')
    cut_str = filename.split("_")[0]
    print cut_str
     #保存切割的图片
    for i in range(0,len(child_img_list)):
        #print child_img_list[i].size    #(28, 28)
        child_img_list[i].save("%s_%s.jpg" % (cut_str[i],random_str(8)))

 
    