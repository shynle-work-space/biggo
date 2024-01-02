import logging
from typing import Literal
from dataclasses import dataclass
# from utils import unix_timestamp_to_tz

class CustomFormatter(logging.Formatter):
    def __init__(self, hostname:str, machine_id:int|float, fmt: str | None = None, datefmt: str | None = None, **kwargs) -> None:
        super().__init__(fmt, datefmt)
        self.hostname = hostname
        self.machine_id = machine_id

    def format(self, record):
        record.hostname = self.hostname
        record.machine_id = self.machine_id
        return super().format(record)


@dataclass
class AppLog:
    hostname: str
    machine_id: str

    def __post_init__(self):
        formatter = CustomFormatter(hostname=self.hostname, machine_id=self.machine_id, fmt='[%(asctime)s] [%(levelname)s] [%(hostname)s] [%(machine_id)s] [%(tag)s] %(message)s', 
                                    datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger("AppLog")
        
        file_log = logging.FileHandler('./logs/app_logs.log')
        file_log.setFormatter(formatter)

        self.logger.addHandler(file_log)
        self.logger.setLevel(logging.NOTSET)

    def __call__(self, msg: str, level:Literal['debug', 'info', 'warning', 'error', 'critical'], tag:str):
        return self.logger.__getattribute__(level)(msg, extra={'tag': tag})


