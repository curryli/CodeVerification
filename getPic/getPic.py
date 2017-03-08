#coding=utf-8
import urllib
#py抓取页面图片并保存到本地

N=5000

c=0
for i in range(N):
	imgurl = 'http://www.sd.10086.cn/portal/login/briefValidateCode.jsp?random=131969.28650689797'
	urllib.urlretrieve(imgurl,r'./getImg/%s.jpg' % c)
	c=c+1

print "get done!"
