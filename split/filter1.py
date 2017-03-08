import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image,ImageEnhance,ImageFilter

img_name = 'sc4.jpg'
#È¥³ý¸ÉÈÅÏß
im = Image.open(img_name)
#Í¼Ïñ¶þÖµ»¯
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
data = im.getdata()
w,h = im.size
#im.show()
black_point = 0
for x in xrange(1,w-1):
    for y in xrange(1,h-1):
        mid_pixel = data[w*y+x] #ÖÐÑëÏñËØµãÏñËØÖµ
        if mid_pixel == 0: #ÕÒ³öÉÏÏÂ×óÓÒËÄ¸ö·½ÏòÏñËØµãÏñËØÖµ
            top_pixel = data[w*(y-1)+x]
            left_pixel = data[w*y+(x-1)]
            down_pixel = data[w*(y+1)+x]
            right_pixel = data[w*y+(x+1)]

            #ÅÐ¶ÏÉÏÏÂ×óÓÒµÄºÚÉ«ÏñËØµã×Ü¸öÊý
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
im.save("sc4_new.jpg")