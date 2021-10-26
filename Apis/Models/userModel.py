import psycopg2
import config as config
from werkzeug.security import generate_password_hash, check_password_hash
from ..common.usermethod import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
import time

SECRET_KEY = 'test'

class Permission(object):
    NOW_ALLLOW = 0
    PERMISSION1 = 1     # 0b000000000000001
    PERMISSION2 = 2  # 0b000000000000010

class User(object):
    def __init__(self, username=None, password=None):
        self.__username = username
        self.__password = password
    
    @property
    def username(self):
        return self.__username

    def password_hash(self):
        self.__password = generate_password_hash(self.__password)

    @classmethod
    def getuserinfo(cls, username):
        try:
            query_doc = {}
            query_doc['username'] = username
            filter = {}
            filter["_id"] = 0
            result = getuserinfo(query_doc, filter)
            return result
        except Exception as e:
            raise e

    def regist(self):
        try:
            userinfo={}
            userinfo['password'] = self.__password
            userinfo['username'] = self.__username
            userinfo['role'] = 'admin'
            userinfo['createtime'] = time.strftime("%Y-%m-%d %H:%M:%S")
            userinfo['status'] = True
            regist(userinfo)
        except Exception as e:
            raise e

    def verify_password(self, password):
        return check_password_hash(password, self.__password)
    
    def generate_auth_token(self, expiration=600):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        # saveToken inredis
        token = s.dumps({'username': self.__username})
        saveToken(self.__username, token.decode(), expiration)
        return token
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except Exception:
            return None    # invalid token
        query_doc = {}
        query_doc['username'] = data['username']
        filter = {}
        filter["_id"] = 0
        user = getuserinfo(query_doc, filter)
        return user
    


            
'''
用户角色权限
'''
class Role(object):
    def __init__(self, userid):
        super().__init__()
        self.userid = userid
    
    @classmethod
    def getRoleInformation(cls, roleid, rolename):
        try:
            result = getroleinfo(roleid, rolename)
            return result
        except Exception as e:
            raise e
    
    def resetPermission(self):
        self.permissions = 0

    def hasPermission(self, perm):
        return self.permissions & perm == perm

    def addPermission(self, perm):
        if not self.hasPermission(perm):
            self.permissions += perm

    def removePermission(self, perm):
        if not self.hasPermission(perm):
            self.permissions -= perm
    



