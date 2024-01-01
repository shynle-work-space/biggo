import jwt
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from dataclasses import dataclass
from errors import Error, DatabaseError 
from typing import TypedDict
from config import config

class JWTPayload(TypedDict):
    id:str

@dataclass
class UserAuthentication:
    config: dict

    def __post_init__(self):
        username = self.config.get('access_usr')
        password = self.config.get('access_pwd')
        host = self.config.get('mariadb_host')
        port = self.config.get('mariadb_port')
        authdb = self.config.get('authdb')
        uri = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{authdb}"
        self.engine = create_engine(uri)
        try:
            connection = self.engine.connect()
            connection.close()
        except DatabaseError:
            print('Cannot connect to MariaDB, closing the server ...')
            exit()


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
        return self.createJWT(result[0], self.config.get('jwt_secret'))
    
    def validate_signature(self, sig:str):
        try:
            decoded:JWTPayload = jwt.decode(sig, self.config.get("jwt_secret"), algorithms=["HS256"])
            return decoded
        except Exception:
            return Error('auth_error', 'Failed to validate token, please login again')