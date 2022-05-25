from flask import Flask, render_template
from flask_socketio import SocketIO, disconnect
from threading import Lock
import json
from PIL import Image

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('connect', namespace='/videodata')
def videostream():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread, 'test')

def background_thread(room):
    count = 0
    while True:
        socketio.sleep(1)
        count+=1
        socketio.emit('server_response', {'data': str(count)}, namespace='/videodata')

@socketio.on('disconnect', namespace='/videodata')
def videostream():
    print('Client disconnected')
    socketio.emit('server_response', {'data': 'disconnect'}, namespace='/videodata')

if __name__ == '__main__':
    # 172.18.27.203
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)