import sys 
from splinter.browser import Browser
    
def main():
    b = Browser(driver_name="chrome")    
    b.visit('https://login.taobao.com/')
    button = b.find_by_xpath("//div[@class='login-switch']")
    button.click()
