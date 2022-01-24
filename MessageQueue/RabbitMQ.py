
import pika 
import json
import config
host = config.MQ_HOST
user = config.MQ_USER
pwd = config.MQ_PASSWORD

class RabbitProducer():
    def __init__(self, host, port, queue, user, password, *args, **kwargs):
        self._host=host
        self._port=port
        self._queue=queue
        self._user=user
        self._password=password
        if 'virtual_host' in kwargs.keys():
            self._virtual_host = kwargs['virtual_host']
        else:
            self._virtual_host = '/'
    
    def connection(self):
        credentials = pika.PlainCredentials(self._user, self._password)
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self._host, port=self._port, virtual_host=self._virtual_host, credentials=credentials)
        )
        return self.__connection.is_open

    def publish_message(self,message):
        channel = self.__connection.channel()
        # # 声明exchange的名字和类型
        # channel.exchange_declare(exchange=exchange, exchange_type='fanout')
        # # 将消息放到“邮筒”
        # channel.basic_publish(exchange=exchange, body=message, routing_key='')
        # 将消息放到邮局
        result = channel.queue_declare(queue=self._queue, durable=True)
        channel.basic_publish(exchange='', routing_key=self._queue, body=message, properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        self.__connection.close()

        

class RabbitComsumer():
    def __init__(self, host, port, queue, user, password, *args, **kwargs):
        self._host=host
        self._port=port
        self._queue=queue
        self._user=user
        self._password=password
        if 'virtual_host' in kwargs.keys():
            self._virtual_host = kwargs['virtual_host']
        else:
            self._virtual_host = '/'
    
    def connection(self):
        credentials = pika.PlainCredentials(self._user, self._password)
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self._host, port=self._port, virtual_host=self._virtual_host, credentials=credentials)
        )
        return self.__connection.is_open
    
    def subscribe(self):
        channel = self.__connection.channel()
        channel.queue_declare(queue=self._queue, durable=False)
        # 设置回调函数
        def callback(ch, method,properties, body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print('receive:'+body.decode())
        channel.basic_consume(self._queue, callback)
        channel.start_consuming()
