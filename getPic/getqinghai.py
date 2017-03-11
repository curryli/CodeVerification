#coding=utf-8
import urllib
#py抓取页面图片并保存到本地

N=50

i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5", \
					"Referer": 'https://qh.ac.10086.cn/servlet/CreateImage?datetime=1489200114127'}
req = urllib2.Request(url, headers=i_headers)

c=0
for i in range(N):
	imgurl = 'https://qh.ac.10086.cn/servlet/CreateImage'
	urllib.urlretrieve(imgurl,r'./getImg/qinghai/%s.jpg' % c)
	c=c+1

print "qinghai done!"
