from config import config
from auth import UserAuthentication
from file_access import FileAccess

authenticator = UserAuthentication(config)
file_access = FileAccess(config)