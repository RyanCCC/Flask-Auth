from flask import Flask
import flask
from Apis import Auth_api

app = Flask(__name__)
app.config['SWAGGER_UI_JSONEDITOR'] = True

Auth_api.init_app(app)

if __name__ == '__main__':
    # 192.168.2.28
    app.run(host = '0.0.0.0', port = 5000,debug=True)