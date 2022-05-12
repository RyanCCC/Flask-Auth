from flask_restplus import Api
from .userApi import user_api
from .messagequeue import msg_queue_api
from .videooperation import api

Auth_api  = Api(
    version='1.0',
    title='登录校验',
    description='实现登录校验，token权限管控',
    prefix='/api',
    doc ='/swagger-ui.html'
)

Auth_api.add_namespace(user_api)
Auth_api.add_namespace(msg_queue_api)
Auth_api.add_namespace(api)