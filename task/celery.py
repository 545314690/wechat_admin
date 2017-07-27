# Optional configuration, see the application user guide.
from celery import Celery

app = Celery('hello', broker='redis://:topcom123@192.168.0.8:6379/10',
             backend='redis://:topcom123@192.168.0.8:6379/11',
             include=['task.tasks'])

app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
