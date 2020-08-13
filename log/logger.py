import logging
import logging.config
import json
import pkgutil
from common.singleton import Singleton


@Singleton
class Logger(object):
    def __init__(self):
        config_json = pkgutil.get_data('log', 'logging.json')
        config = json.loads(config_json.decode('utf-8'))
        logging.config.dictConfig(config)

    def get_logger(self, name='FileLogger'):
        return logging.getLogger(name)
