from config import config
from auth import UserAuthentication
from file_access import FileAccess
from log import AppLog
from socket import gethostname
from random import randint

authenticator = UserAuthentication()
file_access = FileAccess()


app_type = "flask server"
hostname = gethostname()
flask_id = randint(0, 1_000_000_000)

app_log = AppLog(app_type, hostname, flask_id, config)
