from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import json
import getCookies
import os
import myConfig
import requests

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

def login():
    browser.get("http://www.douyu.com/" + myConfig.ROOMNUM)
    #从文本读取cookies
    with open("./cookies.txt",'r', encoding='utf-8') as f:
        cookiesList = json.loads(f.read())
    f.close()
    
    
    for cookie in cookiesList:
        cookies_dict = {
            'domain':'.douyu.com',
            'httpOnly':False,
            'name':cookie.get('name'),
            'path':'/',
            'secure':False,
            'value':cookie.get('value')
        }
        #将cookie添加到browser中
        browser.add_cookie(cookies_dict)
    #刷新网页
    browser.refresh()

def getChp():
    #骂人api
    curseApi = "https://nmsl.chadiao.app/api.php"
    #彩虹屁api
    ChpApi = "https://chp.shadiao.app/api.php"
    response = requests.get(ChpApi)
    return response.text

def sendMessage():    
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#js-player-asideMain > div > div.layout-Player-chat > div > div.ChatSpeak > div.ChatSend > textarea"))
        )
        #获取聊天框当前文本，即抽奖口令
        #currentText = input.get_property('placeholder')
        
        input.clear()
        input.send_keys(getChp())
        input.send_keys(Keys.ENTER)

    except TimeoutException:
        return sendMessage()

def main():
#判断cookies文件是否存在
    if not os.path.exists("./cookies.txt"):
        getCookies.get_cookies()
    login()
    for i in range(0,myConfig.TIMES//myConfig.FREQUENCY):
        print("第"+str(i+1)+"次参与抽奖")
        sendMessage()
        time.sleep(myConfig.FREQUENCY)


if __name__ == "__main__":
    main()