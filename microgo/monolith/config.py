from os import environ
from dotenv import load_dotenv
from typing import TypedDict

load_dotenv()

class Config(TypedDict):
<<<<<<<< HEAD:microgo/monolith/config.py
    run_mode: str
========
    jwt_secret:str

>>>>>>>> 8e7783f (feat: Remove log to mongodb):microgo/monolith/modules/config/__init__.py
    access_usr:str
    access_pwd:str
    mariadb_host:str
    mariadb_port:str
    authdb:str
    jwt_secret:str

config:Config = {
    'jwt_secret': environ.get('JWT_SECRET'),

    'access_usr': environ.get('ACCESS_USR'),
    'access_pwd': environ.get('ACCESS_PWD'),

    'mariadb_host': environ.get('MARIADB_HOST'),
    'mariadb_port': environ.get('MARIADB_PORT'),
    'authdb': environ.get('AUTHDB'),

    # 'BROKER_HOST': environ.get('BROKER_HOST'),
    # 'BROKER_PORT': environ.get('BROKER_PORT'),
    # 'BROKER_VHOST': environ.get('BROKER_VHOST'),
    'mongo_host': environ.get('MONGO_HOST'),
    'mongo_port': environ.get('MONGO_PORT'),
    

}

print(config)