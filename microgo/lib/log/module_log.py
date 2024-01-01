from pymongo import MongoClient
import logging
from log.utils import unix_timestamp_to_tz
from config import config
from dataclasses import dataclass
from typing import Literal


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt: str | None = None, datefmt: str | None = None, **kwargs) -> None:
        super().__init__(fmt, datefmt)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def format(self, record):
        return super().format(record)

class MongoDBHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

        username = config['access_usr']
        pwd = config['access_pwd']
        mongo_host = config['mongo_host']
        mongo_port = config['mongo_port']

        client = MongoClient(f'mongodb://{username}:{pwd}@{mongo_host}:{mongo_port}?authSource=admin', serverSelectionTimeoutMS=5000)
        
        db = client['log']
        self.collection = db['logs']


    def emit(self, record):
        log_entry = {
            'timestamp': unix_timestamp_to_tz(record.created),
            'level': record.levelname,
            'tag': record.tag,
            'message': record.msg,
        }
        self.collection.insert_one(log_entry)


@dataclass
class ModuleLog:
    def __post_init__(self):
        formatter = CustomFormatter('[%(asctime)s] [%(levelname)s] [%(tag)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger("ModuleLog")
        
        mongo_log = MongoDBHandler()
        
        file_log = logging.FileHandler('./logs/module_logs.log')
        file_log.setFormatter(formatter)

        self.logger.addHandler(mongo_log)
        self.logger.addHandler(file_log)
        self.logger.setLevel(logging.NOTSET)

    def __call__(self, msg: str, level:Literal['debug', 'info', 'warning', 'error', 'critical'], tag:str):
        return self.logger.__getattribute__(level)(msg, extra={'tag': tag})