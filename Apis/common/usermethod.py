import psycopg2
import config as config
from .redisdb import RedisClient
from .mongodb import MongoClient

def getuserinfo(query_doc, filter):
    try:
        client = MongoClient(config.MONGODB_HOST, int(config.MONGODB_PORT), username = config.MONGODB_USER, password= config.MONGODB_PASSWORD)
        db = client.database('Agcimai')
        result = db['userinfo'].find_one(query_doc, filter)
        return result
    except Exception as e:
        raise e
    finally:
        client.close()

def getroleinfo(roleid, rolename):
    params = []
    try:
        connection = psycopg2.connect(config.PGSQL_CONNECTSTRING)
        cursor = connection.cursor()
        sql = '''
            select username, password from "role" where roleid = %s 
        '''
        params.append(roleid)
        if rolename is not None:
            sql += ' and rolename = %s '
            params.append(rolename)
        # 执行语句
        cursor.execute(sql,params)
        result = cursor.fetchall()
        connection.commit()
        ret_result = []
        for item in result:
            temp ={}
            temp['username'], temp['password'] = item
            ret_result.append(temp)
        return ret_result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()

def regist(userinfo):
    try:
        client = MongoClient(config.MONGODB_HOST, int(config.MONGODB_PORT), username = config.MONGODB_USER, password= config.MONGODB_PASSWORD)
        db = client.database('Agcimai')
        result = db['userinfo'].insert_one(userinfo)
        return result
    except Exception as e:
        raise e
    finally:
        client.close()
    

'''
使用redis记录token并设置失效时间
'''
def saveToken(user, token, expiration=300):
    redis = RedisClient(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_PASSWORD)
    redis.handle_redis_token(user, token, expiration)
    redis.close()
    
    

            

