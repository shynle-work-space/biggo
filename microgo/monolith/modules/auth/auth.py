import jwt
from datetime import datetime, timedelta
from dataclasses import dataclass

from sqlalchemy import create_engine, text
from sqlalchemy.exc import DatabaseError

from typing import TypedDict

from modules.config import config
from modules.errors import Error

class JWTPayload(TypedDict):
    id:str


@dataclass
class UserAuthentication:

    def __post_init__(self):
        username = config.get('access_usr')
        password = config.get('access_pwd')
        host = config.get('mariadb_host')
        port = config.get('mariadb_port')
        authdb = config.get('authdb')
        uri = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{authdb}"
        self.engine = create_engine(uri)


    def test_mariadb_connection(self):
        try:
            connection = self.engine.connect()
            connection.close()
        except DatabaseError:
            return 'error'


    def get_user(self, username:str, pwd:str):
        with self.engine.connect() as connection:
            stmt = text("SELECT id FROM users WHERE username=:u and pwd=:p")
            result = connection.execute(stmt, {"u":username, "p": pwd}).one_or_none()
        return result

    @staticmethod
    def createJWT(payload:str, secret):
        return jwt.encode({
            "id": payload,
            "exp": datetime.utcnow() + timedelta(minutes=100000),
            "iat": datetime.utcnow()
        }, key=secret)


    def sign_user(self, username:str, pwd:str):
        """
        Return a signed JWT or error
        """
        result = self.get_user(username, pwd)
        if result is None:
            return Error('auth_error', 'User information mismatch')
        return self.createJWT(result[0], config.get('jwt_secret'))
    
    def validate_signature(self, sig:str):
        try:
            decoded:JWTPayload = jwt.decode(sig, config.get("jwt_secret"), algorithms=["HS256"])
            return decoded
        except Exception:
            return Error('auth_error', 'Failed to validate token, please login again')