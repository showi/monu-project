import os
import logging  # @UnusedImport
import logging.config
import time

from monu.conf import conf

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


class MyFilter(logging.Filter):
    def __init__(self, param=None):
        self.param = param

    def filter(self, record):
        # return True
        if self.param is None:
            allow = True
        else:
            allow = self.param not in record.msg
        if allow:
            record.msg = record.msg
        return allow


class UTCFormatter(logging.Formatter):
    converter = time.gmtime


__FN__ = conf.get('log', 'path')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s [monu.%(name)-12s] %(levelname)-6s %(message)s'
        },
        'utc': {
            '()': UTCFormatter,
            'format': '%(asctime)s %(message)s',
        },
        'stream': {
            'format': '[monu.%(name)-12s] %(levelname)-6s %(message)s',
        }
    },
    'filters': {
        'myfilter': {
            '()': MyFilter,
            'param': 'noshow',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['myfilter'],
            'formatter': 'stream'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': __FN__,
            'formatter': 'default'
        }
    },
    'root': {
        'level': conf.get('debug', 'level'),
        'handlers': ['console', 'file']
    },
}

logging.config.dictConfig(LOGGING)

__FORMAT__ = logging.Formatter(
    '%(asctime)s [monu.%(name)-12s] %(levelname)-6s %(message)s')


def getLogger(name):
    return logging.getLogger(name)


log = getLogger('monu')
log.info('Start logging')
