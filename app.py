import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify
from flask_socketio import SocketIO, emit

# Flask 设置
app = Flask(__name__, static_folder='card-flip/out', static_url_path='/')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app , cors_allowed_origins="*")

# 首页路由：返回 React 编译后的 index.html
@app.route('/')
def index():
    print('[🌐] Accessed index.html')
    # return app.send_static_file('index.html')
    return 'Hello World'

# WebSocket 事件：客户端连接
@socketio.on('connect')
def on_connect():
    print('[🔌] Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('[❌] Client disconnected')

# ESP32 发起：CUP 被拿起
@app.route('/lift1')
def cup_lifted():
    print('[🛑] CUP LIFTED event received from ESP32')
    socketio.emit('data', {'message': 'CUP LIFTED'})
    return 'CUP LIFTED received'

# ESP32 发起：CUP 被放下
@app.route('/set1')
def cup_set():
    print('[✅] CUP SET event received from ESP32')
    socketio.emit('data', {'message': 'CUP SET'})
    return 'CUP SET received'

# 可选：预设按钮触发（前端调试用）
@app.route('/trigger1')
def trigger_1():
    print('[🚨] Trigger 1 called')
    socketio.emit('trigger', {'message': 1})
    return 'trigger 1'

@app.route('/trigger5')
def trigger_5():
    print('[🚨] Trigger 5 called')
    socketio.emit('trigger', {'message': 5})
    return 'trigger 5'

@app.route('/trigger9')
def trigger_9():
    print('[🚨] Trigger 9 called')
    socketio.emit('trigger', {'message': 9})
    return 'trigger 9'

# 启动服务
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)