from spider.loggers.log import logger
from .workers import app


@app.task
def add(x, y):
    try:
        return x + y
    except Exception as exc:
        logger.exception('Sending task raised: %r', exc)
        raise add.retry(exc=exc)


@app.task
def test():
    logger.exception('this is a test')


@app.task
def xsum(numbers):
    return sum(numbers)
