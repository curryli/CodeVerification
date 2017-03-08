from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance

im = Image.open("sc1new.jpg")
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(8)
#im = im.convert('1')
im.save("newsc1.jpg")
