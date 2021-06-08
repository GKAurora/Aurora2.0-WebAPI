import socket
from uuid import uuid4
import logging

BASE_VERSION = "0.1.0"

SERVER_NAME = 'Aurora2.0'
SERVER_HOSTNAME = socket.gethostname()
SERVER_VERSION = '@VERSION@'
SERVER_LOG_NAME = f'{SERVER_NAME}_{uuid4().hex[:8]}'
SERVER_LOG_SLOW_TIME = 1000

if SERVER_VERSION in ['@VERSION@', ""]:
    VERSION = BASE_VERSION
else:
    VERSION = SERVER_VERSION

LOGGER_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] [%(pathname)s:%(funcName)s:%(name)s:%(lineno)s] %(message)s'
        },
        'json': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'console_log': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'info_log': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'H',
            'backupCount': 24,
            'formatter': 'json',
            'filename': f'./log/{SERVER_LOG_NAME}.info.log'
        },
        'warn_log': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'H',
            'backupCount': 24,
            'formatter': 'json',
            'filename': f'./log/{SERVER_LOG_NAME}.warn.log'
        },
        'error_log': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'H',
            'backupCount': 24,
            'formatter': 'json',
            'filename': f'./log/{SERVER_LOG_NAME}.error.log'
        },
        'slow_log': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'H',
            'backupCount': 24,
            'formatter': 'json',
            'filename': f'./log/{SERVER_LOG_NAME}.slow.log'
        },
    },
    'loggers': {
        'info_logger': {
            'handlers': ['info_log', 'console_log'],
            'level': 'INFO'
        },
        'warn_logger': {
            'handlers': ['warn_log', 'console_log'],
            'level': 'INFO'
        },
        'error_logger': {
            'handlers': ['error_log', 'console_log'],
            'level': 'INFO'
        },
        'slow_logger': {
            'handlers': ['slow_log', 'console_log'],
            'level': 'INFO'
        }
    }
}

# Get logger configuration
info_log = logging.getLogger('info_logger')
warn_log = logging.getLogger('warn_logger')
error_log = logging.getLogger('error_logger')
slow_log = logging.getLogger('slow_logger')
