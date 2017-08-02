# Optional configuration, see the application user guide.
import os
from datetime import timedelta

from celery import Celery, platforms
from kombu import Exchange, Queue

from spider.config.conf import get_redis_args
# 允许celery以root身份启动
platforms.C_FORCE_ROOT = True
#获取redis配置参数
redis_args = get_redis_args()
worker_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)) + '/logs', 'celery.log')
beat_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)) + '/logs', 'beat.log')

host = redis_args.get('host')
port = str(redis_args.get('port'))
password = redis_args.get('password')
db_broker = str(redis_args.get('broker'))
db_backend = str(redis_args.get('backend'))

url_broker = 'redis://:' + password + '@' + host + ':' + port + '/' + db_broker
url_backend = 'redis://:' + password + '@' + host + ':' + port + '/' + db_backend
tasks = ['spider.task.login', 'spider.task.gather', 'spider.task.keyword', 'spider.task.tasks']
app = Celery('wechat_task', broker=url_broker, backend=url_backend, include=tasks)

app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERYD_LOG_FILE=worker_log_path,
    CELERYBEAT_LOG_FILE=beat_log_path,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACKS_LATE = True,
    CELERY_TASK_PUBLISH_RETRY=True,
    CELERY_TASK_PUBLISH_RETRY_POLICY={
        'max_retries': 3,
        'interval_start': 10,
        'interval_step': 5,
        'interval_max': 20
    },
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_ROUTES={
        'spider.task.tasks.add': {'queue': 'add'},
        'spider.task.tasks.test': {'queue': 'add'},
        'spider.task.login.login_task': {'queue': 'login_queue'},
        'spider.task.gather.history_task': {'queue': 'crawl_history_queue'},
        'spider.task.keyword.keyword_task': {'queue': 'search_keyword_queue'},
        'spider.task.keyword.user_list_crawl_task': {'queue': 'user_list_crawl_queue'},
        'spider.task.wechat_crawl.wechat_user_crawl_task': {'queue': 'wechat_user_crawl_queue'},
        'spider.task.wechat_crawl.wechat_url_crawl_task': {'queue': 'wechat_url_crawl_queue'},
        'spider.task.wechat_crawl.wechat_crawl_task': {'queue': 'wechat_crawl_queue'},
    },
    CELERYBEAT_SCHEDULE={
        # 'add_task': {
        #     'task': 'spider.task.tasks.test',
        #     'schedule': timedelta(seconds=10),
        #     'options': {'queue': 'add'}
        #     # 'options': {'queue': 'add', 'routing_key': 'for_login'}
        # }
    },
    # CELERY_QUEUES=(
    #     Queue('login_queue', exchange=Exchange('login_queue', type='direct'), routing_key='for_login'),
    # ),

)
if __name__ == '__main__':
    app.start()
