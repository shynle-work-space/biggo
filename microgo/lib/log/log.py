import logging
from pymongo import MongoClient
from typing import Literal
from dataclasses import dataclass
from log.utils import unix_timestamp_to_tz

class CustomFormatter(logging.Formatter):
    def __init__(self, app_type:str, hostname:str, machine_id:int|float, fmt: str | None = None, datefmt: str | None = None, **kwargs) -> None:
        super().__init__(fmt, datefmt)
        self.app_type = app_type
        self.hostname = hostname
        self.machine_id = machine_id

    def format(self, record):
        record.app_type = self.app_type
        record.hostname = self.hostname
        record.machine_id = self.machine_id
        return super().format(record)


class MongoDBHandler(logging.Handler):
    def __init__(self, app_type:str, hostname:str, machine_id:int|float, config:dict, level=logging.NOTSET):
        super().__init__(level)

        username = config['access_usr']
        pwd = config['access_pwd']
        mongo_host = config['mongo_host']
        mongo_port = config['mongo_port']

        client = MongoClient(f'mongodb://{username}:{pwd}@{mongo_host}:{mongo_port}?authSource=admin', serverSelectionTimeoutMS=5000)
        
        db = client['log']
        self.collection = db['logs']
        self.app_type = app_type
        self.hostname = hostname
        self.machine_id = machine_id


    def emit(self, record):
        log_entry = {
            'timestamp': unix_timestamp_to_tz(record.created),
            'level': record.levelname,
            'app_type': self.app_type,
            'hostname': self.hostname,
            'machine_id': self.machine_id,
            'tag': record.tag,
            'message': record.msg,
        }
        self.collection.insert_one(log_entry)


@dataclass
class AppLog:
    app_type: str
    hostname: str
    machine_id: str
    config: dict

    def __post_init__(self):
        formatter = CustomFormatter(app_type=self.app_type, hostname=self.hostname, machine_id=self.machine_id, fmt='[%(asctime)s] [%(levelname)s] [%(app_type)s] [%(hostname)s] [%(machine_id)s] [%(tag)s] %(message)s', 
                                    datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger("AppLog")
        
        mongo_log = MongoDBHandler(self.app_type, self.hostname, self.machine_id, self.config)
        file_log = logging.FileHandler('./logs/app_logs.log')
        file_log.setFormatter(formatter)

        self.logger.addHandler(mongo_log)
        self.logger.addHandler(file_log)
        self.logger.setLevel(logging.NOTSET)

    def __call__(self, msg: str, level:Literal['debug', 'info', 'warning', 'error', 'critical'], tag:str):
        return self.logger.__getattribute__(level)(msg, extra={'tag': tag})


