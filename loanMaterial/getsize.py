from PIL import Image

def main():
    filename = r'D:\verify\bxw\bxw4.png'
    img = Image.open(filename)
    imgSize = img.size #Í¼Æ¬µÄ³¤ºÍ¿í
    print imgSize
    maxSize = max(imgSize) #Í¼Æ¬µÄ³¤±ß
    print maxSize
    minSize = min(imgSize) #Í¼Æ¬µÄ¶Ì±ß
    print minSize

if __name__ == '__main__':
    main()
