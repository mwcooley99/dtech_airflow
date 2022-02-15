from airflow.configuration import conf
from sys import stdout



LOG_LEVEL = conf.get('logging', 'LOGGING_LEVEL').upper()
LOG_FORMAT = conf.get('logging', 'LOG_FORMAT')
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'airflow': {
            'format': LOG_FORMAT
        },
    },
    'filters': {
        'mask_secrets': {
            '()': 'airflow.utils.log.secrets_masker.SecretsMasker'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'airflow',
            'stream': stdout,
            'filters': ['mask_secrets']
        },
        'task': {
            'class': 'logging.StreamHandler',
            'formatter': 'airflow',
            'stream': stdout,
            'filters': ['mask_secrets']},
        'processor': {
            'class': 'logging.StreamHandler',
            'formatter': 'airflow',
            'stream': stdout,
            'filters': ['mask_secrets']
        }
    },
    'loggers': {
        'airflow.processor': {
            'handlers': ['processor'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'airflow.task': {
            'handlers': ['task'],
            'level': LOG_LEVEL,
            'propagate': False,
            'filters': ['mask_secrets']
        },
        'flask_appbuilder': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False
        }
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
        'filters': ['mask_secrets']
    }
}