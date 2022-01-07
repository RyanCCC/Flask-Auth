import redis

class RedisMessage():
    def __init__(self, host, port, password, db=0):
        self._host = host
        self._port = port 
        self._password = password
        self._db = db
    
    def connection(self):
        self.__client = redis.StrictRedis(host=self._host, port=self._port, db=self._db, password=self._password)

    def publish(self,topic, message):
        self.__client.publish(topic, message=message)
    
    def subscribe(self, topic):
        ps = self.__client.pubsub()
        # 订阅消息
        ps.subscribe(topic)
        for item in ps.listen():
            if item['type'] == 'message':
                print(item['channel'], item['data'])



