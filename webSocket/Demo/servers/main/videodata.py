from flask_socketio import emit, join_room, leave_room
from .. import socketio
from threading import Lock
import random
thread = None
thread_lock = Lock()


@socketio.on('joined', namespace='/videodata')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = 'test'
    join_room(room)
    emit('status', {'msg':  ' has entered the room.'}, room=room)


def background_thread():
    while True:
        socketio.sleep(2)
        t = random.randint(1, 100)
        socketio.emit('server_response', {'data': t}, namespace='/videodata')

@socketio.on('text', namespace='/videodata')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = message['room']
    emit('message', {'msg':  ':' + message['msg']}, room=room)
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


@socketio.on('left', namespace='/videodata')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = message['room']
    leave_room(room)
    emit('status', {'msg':  ' has left the room.'}, room=room)