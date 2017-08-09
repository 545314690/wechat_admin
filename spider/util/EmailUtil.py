# encoding=utf-8
# 邮件提醒功能
import smtplib
from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

import time

from spider.config.conf import get_emali_conf
from spider.loggers.log import logger

email_conf = get_emali_conf()


class Email(object):
    def __init__(self):
        self.From = email_conf.get('From')
        self.To = email_conf.get('To')
        self.user = email_conf.get('user')
        self.pwd = email_conf.get('pwd')
        self.stmp = email_conf.get('stmp')

    def send_text(self, subject, text):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.From
        msg['To'] = self.To
        body = MIMEText(text)  # 正文
        msg.set_payload(body)
        s = smtplib.SMTP(self.stmp)
        s.login(self.user, self.pwd)
        s.send_message(msg)
        s.quit()


class EmailUtil(object):
    # 记录上次发送邮件时间，２小时内不再发送邮件
    last_remaind_time = 0

    @staticmethod
    def send_email(email_type):
        if 'wechat_login' == email_type:
            EmailUtil.send_wechat_login_remaind()

    @staticmethod
    def send_wechat_login_remaind():
        now = time.time()
        if (now - EmailUtil.last_remaind_time >= 60 * 60 * 2):
            em = Email()
            em.send_text('微信爬虫登录提醒', '没有可用cookie，请及时登录')
            logger.info("发送登录提醒邮件完成")
            EmailUtil.last_remaind_time = time.time()


if __name__ == '__main__':
    EmailUtil.send_wechat_login_remaind()
