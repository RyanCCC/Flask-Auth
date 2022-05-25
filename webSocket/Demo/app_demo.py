from servers import create_app, socketio


'''
Ref:
1. https://github.com/miguelgrinberg/Flask-SocketIO-Chat
2. 文件架构可以参考：https://github.com/miguelgrinberg/socketio-examples
'''

app_socket = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app_socket, debug=True, host='0.0.0.0', port=5000)