#coding=utf-8
import urllib
#py抓取页面图片并保存到本地

N=50

#c=0
#for i in range(N):
#	imgurl = 'https://jx.ac.10086.cn/common/image.jsp?l=857915.3145331955'
#	urllib.urlretrieve(imgurl,r'./getImg/jiangxi/%s.jpg' % c)
#	c=c+1
#
#print "jiangxi done!"


#c=0
#for i in range(N):
#	imgurl = 'https://hb.ac.10086.cn/SSO/img?codeType=0&rand=1488980163186'
#	urllib.urlretrieve(imgurl,r'./getImg/hubei/%s.jpg' % c)
#	c=c+1
#
#print "hubei done!"
#
#c=0
#for i in range(N):
#	imgurl = 'http://hl.10086.cn/authImg?type=0&rand=0.3955738278448997'
#	urllib.urlretrieve(imgurl,r'./getImg/heilongjiang/%s.jpg' % c)
#	c=c+1
#
#print "heilongjiang done!"
#
#c=0
#for i in range(N):
#	imgurl = 'https://fj.ac.10086.cn/common/image.jsp'
#	urllib.urlretrieve(imgurl,r'./getImg/fujian/%s.jpg' % c)
#	c=c+1
#
#print "fujian done!"


#广东有问题，抓不到
#c=0
#for i in range(N):
#	imgurl = 'https://gd.ac.10086.cn/ucs/captcha/image/reade.jsps?sds=1488980356810'
#	urllib.urlretrieve(imgurl,r'./getImg/guangdong/%s.jpg' % c)
#	c=c+1
#
#print "guangdong done!"

#c=0
#for i in range(N):
#	imgurl = 'https://gx.ac.10086.cn/common/image.jsp'
#	urllib.urlretrieve(imgurl,r'./getImg/guangxi/%s.jpg' % c)
#	c=c+1
#
#print "guangxi done!"
#
#c=0
#for i in range(N):
#	imgurl = 'https://login.10086.cn/captchazh.htm?type=12'
#	urllib.urlretrieve(imgurl,r'./getImg/xizang/%s.jpg' % c)
#	c=c+1
#
#print "xizang done!"
#
#c=0
#for i in range(N):
#	imgurl = 'https://he.ac.10086.cn/common/image.jsp'
#	urllib.urlretrieve(imgurl,r'./getImg/hebei/%s.jpg' % c)
#	c=c+1
#
#print "hebei done!"

#湖南不稳定
#c=0
#for i in range(N):
#	imgurl = 'http://www.hn.10086.cn/service/ics/servlet/ImageServlet'
#	urllib.urlretrieve(imgurl,r'./getImg/hunan/%s.jpg' % c)
#	c=c+1
#
#print "hunan done!"

#c=0
#for i in range(N):
#	imgurl = 'https://hi.ac.10086.cn/sso3/common/image.jsp?l=0.5281886753943406'
#	urllib.urlretrieve(imgurl,r'./getImg/hainan/%s.jpg' % c)
#	c=c+1
#
#print "hainan done!"
#
#c=0
#for i in range(N):
#	imgurl = 'https://nm.ac.10086.cn/createVerifyImageServlet?datetime=Wed%20Mar%2008%2022:02:31%20CST%202017'
#	urllib.urlretrieve(imgurl,r'./getImg/neimenggu/%s.jpg' % c)
#	c=c+1
#
#print "neimenggu done!"

#c=0
#for i in range(N):
#	imgurl = 'https://qh.ac.10086.cn/servlet/CreateImage'
#	urllib.urlretrieve(imgurl,r'./getImg/qinghai/%s.jpg' % c)
#	c=c+1
#
#print "qinghai done!"

#c=0
#for i in range(N):
#	imgurl = 'https://sx.ac.10086.cn/common/image.jsp'
#	urllib.urlretrieve(imgurl,r'./getImg/sxTAIYUAN/%s.jpg' % c)
#	c=c+1
#
#print "sxTAIYUAN done!"

#c=0
#for i in range(N):
#	imgurl = 'https://sn.ac.10086.cn/servlet/CreateImage?1'
#	urllib.urlretrieve(imgurl,r'./getImg/SHANXI/%s.jpg' % c)
#	c=c+1
#
#print "SHANXI done!"
#
#c=0
#for i in range(N):
#	imgurl = 'http://www.yn.10086.cn/service/imageVerifyCode?t=new&r=0.05904947007226857'
#	urllib.urlretrieve(imgurl,r'./getImg/yunnan/%s.jpg' % c)
#	c=c+1
#
#print "yunnan done!"

#加密
#c=0
#for i in range(N):
#	imgurl = 'https://gz.ac.10086.cn/aicas/createVerifyImageServlet?1488982295544'
#	urllib.urlretrieve(imgurl,r'./getImg/guizhou/%s.jpg' % c)
#	c=c+1
#
#print "guizhou done!"

c=0
for i in range(N):
	imgurl = 'https://zj.ac.10086.cn/ImgDisp'
	urllib.urlretrieve(imgurl,r'./getImg/zhejiang/%s.jpg' % c)
	c=c+1

print "zhejiang done!"



#tianjing guizhou    data

#chongqing
#https://service.cq.10086.cn/servlet/ImageServlet?random=0.8027723313148617?width=51&height=22&random=0.009994010205033321

#https://hb.ac.10086.cn/       https://hb.ac.10086.cn/SSO/img?codeType=0&rand=1488980163186  湖北
#https://sx.ac.10086.cn/
#https://ln.ac.10086.cn/   meiyou
#https://jl.ac.10086.cn/
#https://hlj.ac.10086.cn/    http://hl.10086.cn/authImg?type=0&rand=0.3955738278448997
#https://js.ac.10086.cn/
#https://zj.ac.10086.cn/
#https://ah.ac.10086.cn/
#https://fj.ac.10086.cn/  https://fj.ac.10086.cn/common/image.jsp  福建
#https://hn.ac.10086.cn/

#   https://gd.ac.10086.cn/ucs/captcha/image/reade.jsps?sds=1488980356810  guangdong
# guangxi      https://gx.ac.10086.cn/common/image.jsp
# gansu  https://login.10086.cn/captchazh.htm?type=12   有汉字  新疆 西藏 吉林一样    https://login.10086.cn/captchazh.htm?type=12
#hebei  https://he.ac.10086.cn/common/image.jsp
#henan  meiyou
#hunan  http://www.hn.10086.cn/service/ics/servlet/ImageServlet
#hainan  https://hi.ac.10086.cn/sso3/common/image.jsp?l=0.5281886753943406
#nmg   https://nm.ac.10086.cn/createVerifyImageServlet?datetime=Wed%20Mar%2008%2022:02:31%20CST%202017
#qinghai  https://qh.ac.10086.cn/servlet/CreateImage
#shanghai  meiyou
#shanxi 山西  https://sx.ac.10086.cn/common/image.jsp

#陕西  https://sn.ac.10086.cn/servlet/CreateImage?1

#yunnan http://www.yn.10086.cn/service/imageVerifyCode?t=new&r=0.05904947007226857

##zhejiang  https://zj.ac.10086.cn/ImgDisp

#guizhou  https://gz.ac.10086.cn/aicas/createVerifyImageServlet?1488982295544