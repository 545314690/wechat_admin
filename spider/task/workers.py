# Optional configuration, see the application user guide.
import os
from datetime import timedelta

from celery import Celery, platforms
from kombu import Exchange, Queue
# 允许celery以root身份启动
# platforms.C_FORCE_ROOT = True

worker_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__))+'/logs', 'celery.log')
beat_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__))+'/logs', 'beat.log')

tasks = ['spider.task.login']
app = Celery('wechat_task', broker='redis://:topcom123@192.168.0.8:6379/10',
             backend='redis://:topcom123@192.168.0.8:6379/11',
             include=tasks)

# app.conf.update(
#     result_expires=3600,
#     task_routes={
#         'task.tasks.add': {'queue': 'q_add'},
#         'spider.task.login.login_task': {'queue': 'login_queue'},
#     },
# )
app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    # CELERY_ENABLE_UTC=True,
    # CELERYD_LOG_FILE=worker_log_path,
    # CELERYBEAT_LOG_FILE=beat_log_path,
    # CELERY_ACCEPT_CONTENT=['json'],
    # CELERY_TASK_SERIALIZER='json',
    # CELERY_RESULT_SERIALIZER='json',
    result_expires=3600,
    task_routes={
        'task.tasks.add': {'queue': 'q_add'},
        'spider.task.login.login_task': {'queue': 'login_queue'},
    },
    # CELERYBEAT_SCHEDULE={
    #     'login_task': {
    #         'task': 'tasks.login.excute_login_task',
    #         'schedule': timedelta(hours=10),
    #         'options': {'queue': 'login_queue', 'routing_key': 'for_login'}
    #     }
    # },
    # CELERY_QUEUES=(
    #     Queue('login_queue', exchange=Exchange('login_queue', type='direct'), routing_key='for_login'),
    # ),

)
if __name__ == '__main__':
    app.start()
