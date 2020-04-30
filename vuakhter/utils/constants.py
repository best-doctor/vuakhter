from __future__ import annotations
import re


INT_RE = re.compile(r'^\d+\Z')
FLOAT_RE = re.compile(r'^\d+\.\d+\Z')
UUID_RE = re.compile(r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z')

DEFAULT_CHUNK_SIZE = 10

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'elasticsearch': {'level': 'CRITICAL', 'propagate': False},
        'requests': {'level': 'CRITICAL', 'propagate': False},
        'urllib3.connectionpool': {'level': 'CRITICAL', 'propagate': False},
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',
    },
}
