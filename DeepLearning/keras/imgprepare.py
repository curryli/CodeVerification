#import modules
import sys
import os
#import tensorflow as tf
from PIL import Image, ImageFilter


def imageprepare(fname):
    """
    This function returns the pixel values.
    The imput is a png file location.
    """
    im = Image.open(fname).convert('L')
    #print fname
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (28, 28), (255)) #creates white canvas of 28x28 pixels
    
    if width > height: #check which dimension is bigger
        #Width is bigger. Width becomes 20 pixels.
        nheight = int(round((20.0/width*height),0)) #resize height according to ratio width
        if (nheight == 0): #rare case but minimum is 1 pixel
            nheight = 1  
        # resize and sharpen
        img = im.resize((20,nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight)/2),0)) #caculate horizontal pozition
        newImage.paste(img, (4, wtop)) #paste resized image on white canvas
    else:
        #Height is bigger. Heigth becomes 20 pixels. 
        nwidth = int(round((20.0/height*width),0)) #resize width according to ratio height
        if (nwidth == 0): #rare case but minimum is 1 pixel
            nwidth = 1
         # resize and sharpen
        img = im.resize((nwidth,20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth)/2),0)) #caculate vertical pozition
        newImage.paste(img, (wleft, 4)) #paste resized image on white canvas
    
    outdir = 'outImgs_test/'
    #print fname.split("\\")[-1]
    labeldir =  fname.split("\\")[0][-1]
    outname = outdir+ labeldir + "\\" +fname.split("\\")[-1]
    #print outname
    newImage.save(outname)
    
if __name__ == '__main__':
    indir = 'test_singlepress/'
    
    dirlist = os.listdir(indir)
    #print dirlist
    for i in range(0,len(dirlist)):
        surdir = os.path.join(indir,dirlist[i])
        #print surdir
        filelist = os.listdir(surdir)
        #print filelist 
        count =0
        for i in range(0,len(filelist)):
            filename = os.path.join(surdir,filelist[i])
            
            if os.path.isfile(filename):
                #print filename
                count = count+1
                print count
                imageprepare(filename)
             