
from hashlib import new
from random import randint
import time
import json
from chaojiying import Chaojiying_Client
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from PIL import Image
import random
import numpy as np

browser = webdriver.Chrome()

# def deal_word_order_verify():
#     '''
#     语序验证码
#     '''
#     import jieba
#     chaojiying = Chaojiying_Client('1107944034', 'chaojiying', '908627')	#用户中心>>软件ID 生成一个替换 96001
# 	im = open('a.jpg', 'rb').read()													#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
# 	postion_list = chaojiying.PostPic(im, 9104)
#     for postion in postion_list:
#        x_pos,y_pos = browser.find_element_by_class_name('geetest_item_img').location
#        browser.m

def deal_slide_verify():
    '''
    滑动验证码
    '''
    pass



def get_cookies():
    #大马猴直播间
    browser = webdriver.Chrome()
    url = "http://www.douyu.com/"
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

def login():
    
    browser.maximize_window()
    url = "https://passport.douyu.com/member/login?"
    browser.get(url)
    time.sleep(1)
    
    switch_to_phone_login = browser.find_element_by_class_name('inputLoginBtn')
    switch_to_phone_login.click()
    sleep(1)
    phoneNum = browser.find_element_by_name('phoneNum')
    phoneNum.send_keys('13720392545')
    password = browser.find_element_by_name('password')
    password.send_keys('123214')
    # login_btn.click()
    login_btn = browser.find_element_by_class_name('btn-sub')
    login_btn.click()
    sleep(2)
    # with open('1.html','w',encoding='utf-8') as f:
    #     f.write(browser.page_source)
    verify_method = 0 # 0为无验证  1为语序  2为滑块  3为其他
    try:
        if browser.find_element_by_class_name('geetest_commit'):
            print('验证方式为语序验证码')
            verify_method = 1
    except:
        pass
    try:
        if browser.find_element_by_class_name('geetest_slider_button'):
            print('验证方式为滑动验证码') 
            verify_method = 2 
    except:
        pass
    sleep(2)
    verifg_img = browser.find_element_by_class_name('geetest_item_img')
    comfire_btn = browser.find_element_by_class_name('geetest_commit')
    x_pos = verifg_img.location.get('x')
    y_pos = verifg_img.location.get('y')
    print(x_pos,type(x_pos))
    print(verifg_img.location)
    print(verifg_img.size)
    browser.save_screenshot('full.png')
    img_obj = Image.open('full.png')
    verify_img_obj = img_obj.crop((x_pos,y_pos,x_pos+verifg_img.size['width'],y_pos+verifg_img.size['height']))
    verify_img_obj.save('tmp.png')
    ActionChains(browser).move_to_element(verifg_img).perform()
    chaojiying = Chaojiying_Client('1107944034', 'chaojiying', '908627')	#用户中心>>软件ID 生成一个替换 96001
    im = open('tmp.png', 'rb').read()													#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    postion_list = chaojiying.PostPic(im, 9005)

    action = ActionChains(browser)
   
    if postion_list.get('err_no') == 0:
        pos_list = postion_list['pic_str'].split('|')
        print(pos_list)
        #由于人机识别导致验证失败，所以改用模拟人点击的运动轨迹
        # for pos in pos_list:
        #     post = pos.split(',')
        #     print('post===========',end=':')
        #     x_pos = int(post[0])
        #     y_pos = int(post[1])
        #     print(x_pos,y_pos)
        #     currend_x_pos = 0
        #     currend_y_pos = 0
        #     for _ in range(10):
        #         action.move_to_element_with_offset(verifg_img,currend_x_pos,currend_y_pos)
        #         currend_x_pos += 10
        #         currend_y_pos += 10
        #     action.move_to_element_with_offset(verifg_img,x_pos,y_pos)
        #     action.click()
        #   sleep(random.random()+randint(1,3))
        all_postion = []
        l1 = []
        for pos in pos_list:
            post = pos.split(',')
            new_pos = [int(post[0])+verifg_img.size['width'],int(post[1])+verifg_img.size['height']]
            all_postion.append(new_pos)
        #从当前的位置移动到下一个坐标的位置
        current_pos = all_postion[0]
        action.move_to_element_with_offset(verifg_img,all_postion[0][0]-verifg_img.size['width'],all_postion[0][1]-verifg_img.size['height'])
        action.click()
        word_len = len(all_postion)
        #将每个坐标之间的位置差记录到列表
        for i in range(len(all_postion)-1):
            tmp_pos = []
            tmp_pos.append(all_postion[i+1][0] - all_postion[i][0]) 
            tmp_pos.append(all_postion[i+1][1] - all_postion[i][1])

            print(tmp_pos)
            l1.append(tmp_pos)
        for i in range(len(l1)):
            curr = l1[i]
            for _ in range(abs(curr[0])):
                
                action.move_by_offset(int(curr[0]/abs(curr[0])),0)
            for _ in range(abs(curr[1])):
                action.move_by_offset(0,int(curr[1]/abs(curr[1])))
            
            action.click()

    action.move_to_element(comfire_btn)
    sleep(random.random()+randint(1,3))
    action.click()
    action.perform()
    
    # if 1 == verify_method:
    #     deal_word_order_verify()
    # elif 2 == verify_method:
    #     deal_slide_verify()

    #判断登录结果
    #登录成功则将cookie写入文件，文件以账号.txt结尾
    #登录失败则将重新进行验证，失败超过5次则放弃
    sleep(100)




login()