from flask import jsonify

class RetCode(object):
    SUCCESS = (0, "访问成功")
    LOGIN_ERROR = (201, "用户名或密码错误")
    PARAMS_ERROR = (203, "参数有误")
    NEED_LOGIN = (401, "您需要登陆")
    PERMISSION_REQUIED = (403, "权限不足")
    PAGE_NOT_FOUND = (404, "此页面不存在")
    SERVER_ERROR = (500, "服务器异常，紧急修复中...")
    USER_NOT_FOUND = (200, "查无此人")


def retJson(status, data=''):
    result = {
        'code':status[0],
        'msg':status[1],
        'data':data
    }
    return jsonify(result)

class ParamsError(Exception):
    def __init__(self, data=None, *args, **kwargs):
        """这个data和返回结果的data有关"""
        super(ParamsError, self).__init__(self, *args, **kwargs)
        self.data = data