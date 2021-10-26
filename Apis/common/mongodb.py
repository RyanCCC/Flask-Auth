import pymongo

class MongoClient():
    def __init__(self, host, port, *args, **kwargs):
        self._mongo = pymongo.MongoClient(host=host, port=port, password=kwargs['password'], username=kwargs['username'])
    
    def database(self, database):
        db= self._mongo[database]
        return db

    def close(self):
        self._mongo.close()