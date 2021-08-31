import sys
sys.path.append('../')
from flask_restplus import Resource, Namespace
from flask import request, make_response, Response
from .common.return_base import retJson, RetCode
from flask_restplus import fields
from .Models import userModel
import json

user_api = Namespace('userAuth', description='用户登录校验模块')

USER_RESOURCE = user_api.model(
    'POIModel',
    {
        'username':fields.String('', Required=True),
        'password':fields.String(default=' ', Required=True)
    }
)

@user_api.route('/userinfo')
class userinfo(Resource):
    def get(self):
        '''获取用户信息'''
        # todo
        return 'success'
    
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

@user_api.route('/token')
class token(Resource):
    def get(self):
        return 'token'


