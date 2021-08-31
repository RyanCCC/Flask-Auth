import psycopg2
import config as config
from werkzeug.security import generate_password_hash, check_password_hash


def getuserinfo(username):
    try:
        connection = psycopg2.connect(config.PGSQL_CONNECTSTRING)
        cursor = connection.cursor()
        sql = '''
            select username, password from user where username = %s
        '''
        params = (username,)
        # 执行语句
        cursor.execute(sql,params)
        result = cursor.fetchall()
        connection.commit()
        return result
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
            

