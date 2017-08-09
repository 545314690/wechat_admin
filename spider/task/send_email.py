# encoding:utf-8

from spider.task.workers import app
from spider.util.EmailUtil import EmailUtil


@app.task(ignore_result=True)
def send_remaind_email_task(email_type):
    EmailUtil.send_email(email_type)


@app.task(ignore_result=True)
def excute_send_remaind_email_task(email_type):
    app.send_task('spider.task.send_email.send_remaind_email_task', args=[email_type],
                  queue='send_remaind_email_queue')
