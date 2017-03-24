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
    print "fname is " + fname
 
    new_w = 25
    new_h = 40

    newImage = im.resize((new_w,new_h), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
     
    outdir = 'testdata_2/'
    #print fname.split("\\")[-1]
    labeldir = fname.split("/")[1]
    outname = outdir+ labeldir + "/" +fname.split("/")[-1]
    print outname
    newImage.save(outname)
    
if __name__ == '__main__':
    indir = './splitedPicsForTest/'
    
    dirlist = os.listdir(indir)
    #print dirlist
    for i in range(0,len(dirlist)):
        surdir = os.path.join(indir,dirlist[i])
        #print surdir
        filelist = os.listdir(surdir)
        #print filelist 
        #count =0
        for i in range(0,len(filelist)):
            filename = os.path.join(surdir,filelist[i])
            
            if os.path.isfile(filename):
                #print "filename is " + filename
                #count = count+1
                #print count
                imageprepare(filename)
             
