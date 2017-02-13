#!/usr/local/bin/python
# -*- coding: utf8 -*-

'''
Created on 2016年9月2日

@author: PaoloLiu
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

def main():
    username = "18516281151"
    rightPW= "tanzhishuju88"
    wrongPW= "tttzzz888"

#   这里的文件路径是webdriver的文件路径
    driver = webdriver.Chrome(executable_path=r"D:\YZtaobao\chromedriver.exe")
    driver.maximize_window()

#   打开网页
    driver.get("https://login.taobao.com/")

#   等待页面的上元素刷新出来 切换到密码登陆
    WebDriverWait(driver, 10).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='login-switch']").is_displayed())
    elem=driver.find_element_by_xpath("//div[@class='login-switch']")
    wtime = random.uniform(2, 3)
    ActionChains(driver).move_to_element(elem).perform()
    time.sleep(wtime)
    ActionChains(driver).move_by_offset(10, 50).perform()
    time.sleep(wtime)
    ActionChains(driver).move_by_offset(-10, -50).perform()
    time.sleep(wtime)
    elem.click()
    time.sleep(wtime)
 
    
##    driver.refresh()
##    time.sleep(1)
##    WebDriverWait(driver, 15).until(lambda the_driver: the_driver.find_element_by_css_selector("#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static").is_displayed())
##    time.sleep(2)
##    elem=driver.find_element_by_css_selector("#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static").click()
##    time.sleep(1)
##    #driver.refresh()
##
##    
##
    WebDriverWait(driver, 15).until(lambda the_driver: the_driver.find_element_by_id("TPL_username_1").is_displayed())
    time.sleep(1)
    elem=driver.find_element_by_id("TPL_username_1")
    elem.send_keys(username)
    time.sleep(1)


##    WebDriverWait(driver, 5).until(lambda the_driver: the_driver.find_element_by_id("nc_1_n1z").is_displayed())
##    elem=driver.find_element_by_id("nc_1_n1z")
##    ActionChains(driver).click_and_hold(on_element=elem).perform()
##    time.sleep(1)
##    ActionChains(driver).move_to_element_with_offset(to_element=elem, xoffset=100, yoffset=50).perform()
##    time.sleep(0.1)
##    ActionChains(driver).move_to_element_with_offset(to_element=elem, xoffset=100, yoffset=50).perform()
##    time.sleep(0.2)
##    ActionChains(driver).move_to_element_with_offset(to_element=elem, xoffset=100, yoffset=50).perform()
##    time.sleep(0.3)
##    ActionChains(driver).move_to_element_with_offset(to_element=elem, xoffset=100, yoffset=50).perform()
##    time.sleep(0.1)
##    ActionChains(driver).move_to_element_with_offset(to_element=elem, xoffset=200, yoffset=50).perform()
##    time.sleep(0.1)
##    ActionChains(driver).release(on_element=elem).perform()
##    time.sleep(1)

##    WebDriverWait(driver, 15).until(lambda the_driver: the_driver.find_element_by_id("J_Quick2Static").is_displayed())
##    time.sleep(1)
##    elem=driver.find_element_by_id("J_Quick2Static")
##    ActionChains(driver).click_and_hold(on_element=elem).perform()
##    time.sleep(1)
##    ActionChains(driver).release(on_element=elem).perform()
##    time.sleep(1)

##    wtime = random.uniform(1, 2) 
##
    for i in range(1):
        WebDriverWait(driver, 5).until(lambda the_driver: the_driver.find_element_by_id("TPL_password_1").is_displayed())
        elem=driver.find_element_by_id("TPL_password_1")
        elem.send_keys(wrongPW)
        time.sleep(wtime)
        
        WebDriverWait(driver, 5).until(lambda the_driver: the_driver.find_element_by_id("J_SubmitStatic").is_displayed())
        time.sleep(wtime)
        elem=driver.find_element_by_id("J_SubmitStatic")
        ActionChains(driver).click_and_hold(on_element=elem).perform()
        time.sleep(wtime)
        ActionChains(driver).release(on_element=elem).perform()
        time.sleep(wtime)
        print i

       

##    WebDriverWait(driver, 5).until(lambda the_driver: the_driver.find_element_by_id("TPL_password_1").is_displayed())
##    elem=driver.find_element_by_id("TPL_password_1")
##    elem.send_keys(wrongPW)
##    time.sleep(wtime)
        


 

    time.sleep(5)    
    #WebDriverWait(driver, 10).until(lambda the_driver: the_driver.find_element_by_id("nc_1_n1z").is_displayed())
    elem=driver.find_element_by_id("nc_1_n1z")
    time.sleep(1)   
    ActionChains(driver).click_and_hold(on_element=elem).perform()
    time.sleep(wtime)

    
    for i in range(50):
        nt = random.uniform(0.001,0.005)
        nl = random.uniform(20,30)
        ActionChains(driver).move_to_element_with_offset(to_element=elem, xoffset=nl, yoffset=0).perform()
        ActionChains(driver).click_and_hold(on_element=elem).perform()
        time.sleep(nt)
    
    ActionChains(driver).release(on_element=elem).perform()
    time.sleep(wtime) 
    time.sleep(3)
        
if __name__ == '__main__':
    pass

    main()
