from PIL import Image

def main():
    filename = r'D:\verify\bxw\bxw4.png'
    img = Image.open(filename)
    imgSize = img.size #ͼƬ�ĳ��Ϳ�
    print imgSize
    maxSize = max(imgSize) #ͼƬ�ĳ���
    print maxSize
    minSize = min(imgSize) #ͼƬ�Ķ̱�
    print minSize

if __name__ == '__main__':
    main()
