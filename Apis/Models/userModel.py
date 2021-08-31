import psycopg2
import config as config
from werkzeug.security import generate_password_hash, check_password_hash
from ..common.usermethod import *


class User(object):
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
    
    @property
    def password(self):
        return AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def getuserinfo(self):
        try:
            result = getuserinfo(self.__username)
            return result
        except Exception as e:
            raise e

    def regist(self):
        try:
            regist(self.__username, generate_password_hash(self.__password))
        except Exception as e:
            raise e
            

