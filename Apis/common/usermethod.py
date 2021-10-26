import psycopg2
import config as config
from .redisdb import RedisClient

def getuserinfo(username, password=None):
    params = []
    try:
        connection = psycopg2.connect(config.PGSQL_CONNECTSTRING)
        cursor = connection.cursor()
        sql = '''
            SELECT u.userid, up.permissionid, u.username, per.permissionname, per.permissioncode, u.password FROM "user" u inner join "user_permission" up on u.userid = up.userid\
                 inner join "permission" per on per.permissionid = up.permissionid where u.username = %s
        '''
        params.append(username)
        if password is not None:
            sql += ' and u.password = %s '
            params.append(password)
        # 执行语句
        cursor.execute(sql,params)
        result = cursor.fetchall()
        connection.commit()
        ret_result = {}
        if len(result)>0:
            ret_result['userid'], ret_result['permissionid'], ret_result['username'], ret_result['permissionname'], ret_result['permissioncode'], ret_result['password'] = result[0]
        return ret_result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()

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

def regist(username, password):
    try:
        connection = psycopg2.connect(config.PGSQL_CONNECTSTRING)
        cursor = connection.cursor()
        # 目标的明细
        sql = '''
            insert into "user"(username, password) values (%s, %s)
        '''
        
        params = (username, password, )
        # 执行提交事务
        cursor.execute(sql,params)
        connection.commit()
        return True
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()
    

'''
使用redis记录token并设置失效时间
'''
def saveToken(user, token, expiration=300):
    redis = RedisClient(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_PASSWORD)
    redis.handle_redis_token(user, token, expiration)
    
    

            

