import psycopg2
import config as config
from werkzeug.security import generate_password_hash, check_password_hash


def getuserinfo(username, password=None):
    params = []
    try:
        connection = psycopg2.connect(config.PGSQL_CONNECTSTRING)
        cursor = connection.cursor()
        sql = '''
            select username, password from "user" where username = %s 
        '''
        params.append(username)
        if password is not None:
            sql += ' and password = %s '
            params.append(password)
        # 执行语句
        cursor.execute(sql,params)
        result = cursor.fetchall()
        connection.commit()
        ret_result = {}
        if len(result)>0:
            ret_result['username'], ret_result['password'] = result[0]
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
            

