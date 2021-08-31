from flask_restplus import Api
from .user import user_api

Auth_api  = Api(
    version='1.0',
    title='登录校验',
    description='实现登录校验，token权限管控',
    prefix='/api',
    doc ='/swagger-ui.html'
)

Auth_api.add_namespace(user_api)