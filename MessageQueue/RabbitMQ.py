
import pika 
import json
import config
host = config.MQ_HOST
user = config.MQ_USER
pwd = config.MQ_PASSWORD

class RabbitProducer():
    def __init__(self):
        pass
        

class RabbitComsumer():
    def __init__(self):
        pass


def publish_message(MQ_INFO, message):
    credentials = pika.PlainCredentials(MQ_INFO['user'],MQ_INFO['password'])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=MQ_INFO['host'], port=MQ_INFO['port'], virtual_host='/', credentials=credentials)
    )
    channel = connection.channel()
    # 声明消息队列
    result = channel.queue_declare(queue=MQ_INFO['queue'])
    channel.basic_publish(exchange='', routing_key=MQ_INFO['queue'], body=message)
    connection.close()

