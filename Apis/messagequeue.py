import flask
from MessageQueue import RabbitMQ, redisMQ
import json
from flask import request
import config
from flask_restplus import Resource, Namespace, fields

msg_queue_api = Namespace('MsgQueue', description='消息队列')
host = config.MQ_HOST
user = config.MQ_USER
pwd = config.MQ_PASSWORD


MSG_RESOURCE = msg_queue_api.model(
    'MessageModel',
    {
        'queue':fields.String('', Required=True),
        'message':fields.String(default=' ', Required=True) 
    }
)

@msg_queue_api.route('/test')
class Test(Resource):
    def get(self):
        '''测试接口'''
        return 'hello message queue.'

@msg_queue_api.route('/producer')
class MsgQueuePublish(Resource):
    @msg_queue_api.doc(params={'message':'', 'queue':''})
    def get(self):
        '''用rabbitmq做消息队列'''
        message = request.args.get('message')
        queue = request.args.get('queue')
        client = RabbitMQ.RabbitProducer(host, '5672', queue, user, pwd)
        client.connection()
        client.publish_message(message)
        return 'success'
    
    @msg_queue_api.expect(MSG_RESOURCE)
    def post(self):
        '''用redis做消息队列'''
        req_data = json.loads(request.data.decode())
        queue = req_data['queue']
        message = req_data['message']
        msg_queue = redisMQ.RedisMessage(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_PASSWORD)
        msg_queue.connection()
        # msg_queue.publish(queue,'hello world')
        msg_queue.publish(queue, message)
        return 'success'