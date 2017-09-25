# encoding=utf-8
from selenium import webdriver
import time

from spider.db.redis_db import Cookies
from spider.loggers.log import login
from spider.service.common import get_token_by_cookies
#download form https://chromedriver.storage.googleapis.com/2.27/chromedriver_linux64.zip
account_xpath = '//*[@id="header"]/div[2]/div/div/form/div[1]/div[1]/div/span/input'
pwd_xpath = '//*[@id="header"]/div[2]/div/div/form/div[1]/div[2]/div/span/input'
login_btn_xpath = '//*[@id="header"]/div[2]/div/div/form/div[4]/a'
wechat_login_page = 'https://mp.weixin.qq.com/'
def do_wechat_login(name, password):
    post = {}

    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    driver.get(wechat_login_page)
    time.sleep(2)
    driver.find_element_by_xpath(account_xpath).clear()
    driver.find_element_by_xpath(account_xpath).send_keys(name)
    driver.find_element_by_xpath(pwd_xpath).clear()
    driver.find_element_by_xpath(pwd_xpath).send_keys(password)
    # 在自动输完密码之后记得点一下记住我
    time.sleep(5)
    # driver.find_element_by_xpath("./*//a[@id='loginBt']").click()
    # yzm = input("Please input your 验证码:\n")
    # driver.find_element_by_xpath("./*//input[@id='verify']").send_keys(yzm)
    driver.find_element_by_xpath(login_btn_xpath).click()
    # 拿手机扫二维码！
    time.sleep(15)
    driver.get(wechat_login_page)
    cookie_items = driver.get_cookies()
    for cookie_item in cookie_items:
        post[cookie_item['name']] = cookie_item['value']
    # 判断是否登录成功,保存cookie
    if (post['data_ticket'] != None):
        #根据cookies 获取token，只需要带上cookie访问首页
        token = get_token_by_cookies(post)
        post['token'] = token
        #保存cookie
        Cookies.store_cookies(name, post)
        login.info(name + "登录成功！")
    else:
        login.error(name + "登录失败！")
        # cookie_str = json.dumps(post)
        # with open('cookie.txt', 'w+', encoding='utf-8') as f:
        #     f.write(cookie_str)


# cookie 的数据格式说明
cookie = {"remember_acct": "812690341%40qq.com",
          "openid2ticket_oEvZHwwoohqvrzfanzFlGtnjKzOU": "epYhuy0qKXlUCgDcAVo1O0j/PpM1DCMJ7gBTi9l9Oj8=",
          "data_ticket": "q8b4AvAIyJI1aP2bUOJnSDN+Hk6jD+Pgj0Ltb7aoKF2xvWUE78bhYNfV56ULb/o5",
          "ticket": "dcb9a9cde12edfd6bb4df55ce643d9ccf8454322",
          "bizuin": "3216335643",
          "slave_sid": "YjNGbWJVNVNMRnE4NGppVW5OVmhEM1h3bGhIMmloem5qN1UyUHc3c1VPT2FrN2tiOUs2aVMxNTRPbGFWVGxIa25WaE1pNmdoVmdwclZCVmlSbWtyRFFhTXZjMVl5RV9hNHVzM1p3MU5LX0lNeTM0bVkxU1pndVQzU1ZYT1hnd2I4R3QyaWxHWDQ2Z0xqYnR5",
          "ticket_id": "gh_74a4472884e4",
          "uuid": "277cb41583b4791332b3cb0358250455",
          "slave_user": "gh_74a4472884e4",
          "ua_id": "C40K1LYiZaBvGtndAAAAAGOT8emf5SpEluNQFFPrchg=",
          "xid": "c2cf56ba403643c6ec332d3a000fb4a3",
          "pgv_pvi": "2749064192",
          "pgv_si": "s3492151296",
          "cert": "IL6NfYLHwW_OEBEyMQT9Mbpzq7dQywKD",
          "noticeLoginFlag": "1",
          "data_bizuin": "3276273170"
          }
