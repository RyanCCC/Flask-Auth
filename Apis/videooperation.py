import sys
sys.path.append('../')
from flask_restplus import Resource, Namespace
from werkzeug.datastructures import FileStorage
from flask import request, Response
from camera.camera_opencv import Camera



api = Namespace('VideoOperation', description='视频上传下载基本操作')
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required = True)
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'flv', 'wmv', 'rm','rmb'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def gen(camera):
    """Video streaming generator function."""
    while True:
        try:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            raise(e)

@api.route('/video')
class video(Resource):
    @api.doc(params={'videoname':'视频名称'})
    def get(self):
        '''测试视频'''
        try:
            videoname = request.args.get('videoname')
            camera = Camera(videoname)
            if camera.thread is None:
                raise RuntimeError('Could not start camera. Please check your video name.')
            return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
        except Exception as e:
            result = {}
            result['code'] = 500
            result['message'] = str(e)
            return result