# coding:utf-8
import logging.config
import os
import logging.config as log_conf

log_dir = os.path.dirname(os.path.dirname(__file__)) + '/logs'
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

log_path = os.path.join(log_dir, 'wechat.log')

log_config = {
    'version': 1.0,
    'formatters': {
        'detail': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detail'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'filename': log_path,
            'level': 'INFO',
            'formatter': 'detail',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'crawler': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'parser': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'other': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'storage': {
            'handlers': ['file'],
            'level': 'INFO',
        }
    }
}

log_conf.dictConfig(log_config)

logger = logging.getLogger(__name__)
login = logging.getLogger('login')
search = logging.getLogger('search')
crawler = logging.getLogger('crawler')
parser = logging.getLogger('page_parser')
storage = logging.getLogger('storage')
other = logging.getLogger('other')

__all__ = ['login', 'logger', 'crawler', 'parser', 'search', 'storage', 'other']
