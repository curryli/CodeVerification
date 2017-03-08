# -*- coding: utf-8 -*-
from PIL import Image,ImageEnhance,ImageFilter

def cut_pic(filename):  #图片处理（灰度化，二值化，切割图片）
     filepath = filename
     im = Image.open(filepath)
     imgSize = im.size #
     print imgSize   #(130, 50)
     imgry = im.convert('L')  #灰度化
     #imgry.show()
     #二值化
     threshold = 130
     table = []
     realcut = []
     for i in range(256):
         if i <threshold:
             table.append(0)
         else:
             table.append(1)
     biPic = imgry.point(table,'1')
     bi_w = biPic.width    
     bi_h = biPic.height
      
      
     #保存要切割的列
     box = (5, 6, bi_w-13, bi_h-16)  # left, upper, right, lower 
     out = biPic.crop(box)
     print out.size #(110, 30)
     out.show()
    
     out_w = out.width
     out_h = out.height
     
     realcut = [0, out_w/4, out_w/2, 3*out_w/4, out_w]
     print realcut
     #切割图片
     count = [0,1,2,3]
     child_img_list = []
     for i in count:
         child_img = out.crop((realcut[i],0,realcut[i+1],out_h))
         child_img_list.append(child_img)
    
     # 返回切割的图片
     return child_img_list
     
if __name__ == '__main__':
    child_img_list = cut_pic('newsc1.jpg')
    
     #保存切割的图片
    for i in range(0,len(child_img_list)):
        print child_img_list[i].size    #(28, 28)
        child_img_list[i].save("b%d.jpg" % i)
 
    