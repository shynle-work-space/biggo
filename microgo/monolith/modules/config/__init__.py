from os import environ
from dotenv import load_dotenv
from typing import TypedDict

if environ.get('RUN_MODE') == 'development':
    load_dotenv('./.env')

class Config(TypedDict):
    jwt_secret:str

    access_usr:str
    access_pwd:str
    
    mariadb_host:str
    mariadb_port:str
    authdb:str
    
    mongo_host:str
    mongo_port:str

config:Config = {
    'jwt_secret': environ.get('JWT_SECRET'),

    'access_usr': environ.get('ACCESS_USR'),
    'access_pwd': environ.get('ACCESS_PWD'),

    'mariadb_host': environ.get('MARIADB_HOST'),
    'mariadb_port': environ.get('MARIADB_PORT'),
    'authdb': environ.get('AUTHDB'),

    'mongo_host': environ.get('MONGO_HOST'),
    'mongo_port': environ.get('MONGO_PORT'),
    

}