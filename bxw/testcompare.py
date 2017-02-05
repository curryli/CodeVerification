import cv2
import numpy as np
 
img = cv2.imread('material/bxw5_1.png',0)
img2 = img.copy()
template = cv2.imread("full/9_0.png",0)
 

### All the 6 methods for comparison in a list
##methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
##            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
##
##for meth in methods:
##    img = img2.copy()
##    method = eval(meth)
##
##    # Apply template Matching
##    res = cv2.matchTemplate(img,template,method)
##    print res


img = img2.copy()
meth = 'cv2.TM_CCOEFF_NORMED'
method = eval(meth)

res = cv2.matchTemplate(img,template,method)
print res[0][0]
