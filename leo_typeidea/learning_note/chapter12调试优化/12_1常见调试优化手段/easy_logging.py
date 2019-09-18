import logging
from logging.config import dictConfig

logging_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s%(name)-12s %(levelname)-8s %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': "default",
            'level': logging.DEBUG
        },
        'simple_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': logging.WARNING
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': logging.DEBUG,
        },
        'simple': {
            'handlers': ['simple_console'],
            'level': logging.ERROR,
            'propagate': False
        }
    },
}

dictConfig(logging_config)
logger = logging.getLogger(__name__)
logger.debug('这是debug级的log:%s', 'debug')
logger.error('这是error级的log:%s', 'error')

simple_logger = logging.getLogger('simple')
simple_logger.debug('这是debug级的log')
simple_logger.error('这是error级的log')
