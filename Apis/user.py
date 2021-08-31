import sys
from typing_extensions import final
sys.path.append('../')
from flask_restplus import Resource, Namespace
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import request, make_response, Response

user_api = Namespace('VideoOperation', description='视频上传下载基本操作')