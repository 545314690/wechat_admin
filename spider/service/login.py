from selenium import webdriver
import time
import json

from spider.db.redis_db import Cookies


def do_login(name, password):
    post = {}

    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    driver.get('https://mp.weixin.qq.com/')
    time.sleep(2)
    driver.find_element_by_xpath("./*//input[@id='account']").clear()
    # driver.find_element_by_xpath("./*//input[@id='account']").send_keys('962401440@qq.com')
    driver.find_element_by_xpath("./*//input[@id='account']").send_keys(name)
    driver.find_element_by_xpath("./*//input[@id='pwd']").clear()
    # driver.find_element_by_xpath("./*//input[@id='pwd']").send_keys('lyc123456')
    driver.find_element_by_xpath("./*//input[@id='pwd']").send_keys(password)
    # 在自动输完密码之后记得点一下记住我
    time.sleep(5)
    # driver.find_element_by_xpath("./*//a[@id='loginBt']").click()
    # yzm = input("Please input your 验证码:\n")
    # driver.find_element_by_xpath("./*//input[@id='verify']").send_keys(yzm)
    driver.find_element_by_xpath("./*//a[@id='loginBt']").click()
    # 拿手机扫二维码！
    time.sleep(15)
    driver.get('https://mp.weixin.qq.com/')
    cookie_items = driver.get_cookies()
    for cookie_item in cookie_items:
        post[cookie_item['name']] = cookie_item['value']
    cookie_str = json.dumps(post)
    Cookies.store_cookies(name,post)
    with open('cookie.txt', 'w+', encoding='utf-8') as f:
        f.write(cookie_str)
