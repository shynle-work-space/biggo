from socket import gethostname
from random import randint

from modules.log import AppLog
from modules.auth import UserAuthentication
from microgo.file_access import FileAccess
from modules.config import config



hostname = gethostname()
flask_id = randint(0, 1_000_000_000)
app_log = AppLog(hostname=hostname, machine_id=flask_id)
authenticator = UserAuthentication()
file_access = FileAccess(config)


app_log(f'Server start in {hostname} with id {flask_id}', 'info', tag='server start')


