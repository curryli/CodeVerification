# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from PIL import Image,ImageEnhance,ImageFilter
import urllib
import time
import random
import re




if __name__ == '__main__':
#   这里的文件路径是webdriver的文件路径
    driver = webdriver.Chrome(executable_path=r"D:\CodeVerification\tools\chromedriver.exe")
    driver.maximize_window()
    
#   打开网页
    driver.get("http://www.sc.10086.cn/service/login.html?url=index.html?ts=1488957604650")
    
    WebDriverWait(driver, 10).until(lambda the_driver: the_driver.find_element_by_id("fwtpyzm").is_displayed())
    elem = driver.find_element_by_id("fwtpyzm")
    
 
    time.sleep(1)
    print "Done"
    driver.save_screenshot('tmp.png')   
    
    
    location = elem.location
    print location['x'], location['y'] 
    
    rangle = (location['x'], location['y'], location['x']+107, location['y']+30)
    i = Image.open('tmp.png')
    frame4 = i.crop(rangle)
    frame4.save('authcode.png')
    
    print "Done"
    
    
 
