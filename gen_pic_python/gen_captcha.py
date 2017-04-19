# -*- coding: utf-8 -*-
import sys
import random  
import string  
from PIL import Image,ImageDraw,ImageFont,ImageFilter  
  
#字体的位置，不同版本的系统会有不同  
font_path = "Fonts/ARIALNB.TTF"  
#生成几位数的验证码  
number = 4  
#生成验证码图片的高度和宽度  
size = (100,30)  
#背景颜色，默认为白色  
bgcolor = (255,255,255)  
#字体颜色，默认为蓝色   
fontcolor = (0,0,255)  
#干扰线颜色。默认为红色  
linecolor = (255,0,0)  
#是否要加入干扰线  
draw_line = True  
#加入干扰线条数的上下限  
line_number = (1,5)  
  
#用来随机生成一个字符串  
def gene_text():  
    source = list(string.letters)  
    for index in range(0,10):  
        source.append(str(index))  
    nums = random.sample(source,number)  
    text = ''.join(nums)  
    return text  
  
#用来绘制干扰线  
def gene_line(draw,width,height):  
    line_num = random.randint(line_number[0],line_number[1])  
    for i in range(line_num):  
        begin = (random.randint(0, width), random.randint(0, height))  
        end = (random.randint(0, width), random.randint(0, height))  
        draw.line([begin, end], fill = linecolor)  
  
#生成验证码  
def gene_code():  
    width,height = size #宽和高  
    image = Image.new('RGB',(width,height),bgcolor) #创建图片  
    font = ImageFont.truetype(font_path,30) #验证码的字体  
    draw = ImageDraw.Draw(image)  #创建画笔  
    text = gene_text() #生成字符串  
    font_width, font_height = font.getsize(text)  
    draw.text(((width - font_width) / number, (height - font_height) / number),text, font=font,fill=fontcolor) #填充字符串  
    if draw_line:  
        gene_line(draw,width,height)  
    params = [1 - float(random.randint(1, 2)) / 100,  0,   0,  0,  1 - float(random.randint(1, 10)) / 100,  float(random.randint(1, 2)) / 500,  0.001,  float(random.randint(1, 2)) / 500]  
    image = image.transform(size, Image.PERSPECTIVE, params) #创建扭曲  
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE) #滤镜，边界加强  
    image.save('4.jpeg') #保存验证码图片  
  
if __name__ == "__main__":  
    gene_code()  