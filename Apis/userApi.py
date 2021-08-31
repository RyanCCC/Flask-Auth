import sys
import flask
sys.path.append('../')
from flask_restplus import Resource, Namespace
from flask import request, make_response, Response
from .common.return_base import retJson, RetCode
from flask_restplus import fields
from .Models import userModel
import json
from flask_httpauth import HTTPTokenAuth


user_api = Namespace('userAuth', description='用户登录校验模块')

USER_RESOURCE = user_api.model(
    'POIModel',
    {
        'username':fields.String('', Required=True),
        'password':fields.String(default=' ', Required=True)
    }
)
token_auth = HTTPTokenAuth(scheme='Bearer')

@token_auth.verify_token
def verify_token(token):
    user = userModel.User.verify_auth_token(token)
    if not user:
        return False
    return True

@token_auth.error_handler
def tokenUnauthorized():
    return retJson(RetCode.NEED_LOGIN)

@user_api.route('/userinfo')
class userinfo(Resource):
    @user_api.doc(params={'username':''})
    def get(self):
        '''获取用户信息'''
        username = request.args.get('username')
        result = userModel.User(username=username).getuserinfo(username)
        return result
    
    @user_api.expect(USER_RESOURCE)
    def post(self):
        '''注册新的用户信息'''
        req_data = json.loads(request.data.decode())
        username = req_data['username']
        password = req_data['password']
        if None in (username, password):
            return retJson(RetCode.PARAMS_ERROR)
        else:
            userinfo = userModel.User(username, password)
            userinfo.password_hash(password)
            userinfo.regist()
        return 'success'
    
    def put(self):
        '''修改用户信息'''
        # TODO
        return 'success'

    def delete(self):
        '''删除用户信息'''
        #TODO
        return 'success'


@user_api.route('/userrole')
class userrole(Resource):
    def get(self):
        '''获取角色信息'''
        return 'admin'

@user_api.route('/login')
class token(Resource):
    @user_api.doc(params={'username':'', 'password':''})
    def get(self):
        username = request.args.get('username')
        password = request.args.get('password')
        user = userModel.User(username=username, password=password)
        # 登录校验
        userinfo = user.getuserinfo(username=username)
        flag = user.verify_password(userinfo['password'])
        if flag:
            token = user.generate_auth_token()
            return token.decode()
        else:
            return retJson(RetCode.LOGIN_ERROR)
    @user_api.expect(USER_RESOURCE)
    def post(self):
        req_data =json.loads(request.data.decode())
        username = req_data['username']
        password = req_data['password']
        user = userModel.User(username, password)(password)
        return user

user_id_header_parser  = user_api.parser()
user_id_header_parser .add_argument('Authorization', location='headers')

@user_api.expect(user_id_header_parser)
@user_api.route('/helloworld')
class helloworld(Resource):
    @token_auth.login_required()
    def get(self):
        return 'helloworld'



