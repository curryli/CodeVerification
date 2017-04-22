# -*- coding: utf-8 -*-
#导入三个模块
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

'''基本功能'''
_letter_cases = "abcdefghjkmnpqrstuvwxy" # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper() # 大写字母
_numbers = ''.join(map(str, range(3, 10))) # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))


#图片宽度、高度
#width = 15
#height = 30
#背景颜色
bgcolor = (255,255,255)

#加载字体
font_path = "Fonts/ARIALNB.TTF"  
font = ImageFont.truetype(font_path,30)
#字体颜色
fontcolor = (0,0,0)
gene_str = random.sample(init_chars, 1)     
gene_char = gene_str[0]
print gene_char 
     
font_width, font_height =  font.getsize(gene_char)   
#print font_width, font_height

Pic_width = int(font_width*1.1)
Pic_height = int(font_height*0.9)

#产生draw对象，draw是一些算法的集合
#生成背景图片
image = Image.new('RGBA',(Pic_width,Pic_height), bgcolor)
draw = ImageDraw.Draw(image)
#画字体,(0,0)是起始位置
'''生成给定长度的字符串，返回列表格式'''
#random.sample(chars, length)
 
#draw.text((0, -(Pic_height - font_height)), gene_char, font=font, fill=fontcolor)
start_x = (Pic_width - font_width) / 3
start_y = (Pic_height - font_height)
#print start_x,start_y
draw.text((start_x, start_y), gene_char, font=font, fill=fontcolor)
#释放draw
del draw
#保存原始版本
#image.save('2_1.png')


'''演示扭曲，需要新建一个图片对象  http://www.bubuko.com/infodetail-641617.html  '''
rot = image.rotate(random.randint(-10,10),expand=0) #默认为0，表示剪裁掉伸到画板外面的部分
fff = Image.new('RGBA',rot.size,(255,)*4)
image = Image.composite(rot,fff,rot)
#print image.size
#image.save('2_2.png')
image = image.resize((28,28))
#print image.size
image.save('2_2.png')




 