import psycopg2
import config as config
from werkzeug.security import generate_password_hash, check_password_hash
from ..common.usermethod import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired

SECRET_KEY = 'agcimai'

class User(object):
    def __init__(self, username=None, password=None):
        self.__username = username
        self.__password = password
        # self.password_hash = generate_password_hash(password)
    
    @property
    def username(self):
        return self.__username

    def password_hash(self, password):
        self.__password = generate_password_hash(self.__password)

    @classmethod
    def getuserinfo(cls, username):
        try:
            result = getuserinfo(username)
            return result
        except Exception as e:
            raise e

    def regist(self):
        try:
            regist(self.__username, self.__password)
        except Exception as e:
            raise e
    
    def verify_password(self, password):
        return check_password_hash(password, self.__password)
    
    def generate_auth_token(self, expiration=600):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return s.dumps({'username': self.__username})
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except Exception:
            return None    # invalid token
        user = getuserinfo(data['username'])
        return user

            

