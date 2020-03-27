from selenium import webdriver
import time
import json
import myConfig



def get_cookies():
    #大马猴直播间
    browser = webdriver.Chrome()
    url = "http://www.douyu.com/"+myConfig.ROOMNUM
    browser.get(url)
    #在20秒内完成扫码登录，来获取Cookies
    #若未登录成功则启动失败
    time.sleep(20)
    dictCookies =  browser.get_cookies()
    jsonCookies = json.dumps(dictCookies)
    with open("./cookies.txt",'w') as f:
        f.write(jsonCookies)
    f.close()
    browser.close()
