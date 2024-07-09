'''
@Date         : 2020-11-13 16:46:20
@LastEditors  : Pineapple
@LastEditTime : 2020-11-14 09:10:00
@FilePath     : /database_pool/sqlhelper2.py
@Blog         : https://blog.csdn.net/pineapple_C
@Github       : https://github.com/Pineapple666
'''
import pymysql
from dbutils.pooled_db import PooledDB
from conf.server_config import SERVER_CONFIG
import traceback
class SqlHelper:
    def __init__(self) -> None:
        self.pool = PooledDB(
            creator=pymysql,  # 使用pymysql作为连接的创建者
            maxconnections=20,  # 连接池中最大连接数
            mincached=2,  # 连接池中最小空闲连接数
            maxcached=20,  # 连接池中最大空闲连接数
            maxshared=20,  # 连接池中最大共享连接数
            blocking=True,  # 如果连接池达到最大连接数，是否等待连接释放后再获取新连接
            host=SERVER_CONFIG['DBConfig'].HOSTNAME,  # 数据库主机名
            port=SERVER_CONFIG['DBConfig'].PORT,  # 数据库端口号
            user=SERVER_CONFIG['DBConfig'].USERNAME,  # 数据库用户名
            password=SERVER_CONFIG['DBConfig'].PASSWORD,  # 数据库密码
            database=SERVER_CONFIG['DBConfig'].DATABASE,  # 数据库名称
            charset='utf8mb4'  # 数据库字符集
        )

        self.dbname = 'SD_TASK_EXCHAGE'#SERVER_CONFIG['DBConfig'].DATABASE

    def get_task_by_requestid(self, requestid):
        with self as db:
            try:
                sql = "select * from %s where requestid='%s'" %(self.dbname,requestid)
                db.cursor.execute(sql)
                print(sql,"  \nget_task_by_requestid 查询成功！！！！")
                return db.cursor.fetchone()
            except Exception as e:
                traceback.print_exc()
                print("get_task_by_status error~:", e)

    # 数据库的查询操作
    def get_task_by_status(self, status,num=5):
        with self as db:
            try:
                sql= "select * from %s where status=%d limit %d" % (self.dbname, status,num)
                db.cursor.execute(sql)
                res = db.cursor.fetchall()
                if res:
                    return res
            except Exception as e:
                traceback.print_exc()
                print("get_task_by_status error~:", e)



    def create_task(self, obj):
        with self as db:
            sql = f""" INSERT INTO %s (requestid,image,image2, model_param,cnt,status)
                        VALUES('%s','%s','%s','%s',%d,1)""" % (self.dbname, obj['requestid'], obj['image'], obj['image2'], obj['model_param'],obj['cnt'])
            try:
                db.cursor.execute(sql)
                db.conn.commit()
            except Exception as e:
                db.conn.rollback()
                traceback.print_exc()
            print("插入成功！！！！")

    # 数据库更新操作
    def update_task(self, obj):
        with self as db:
            print("sql update_task :",obj)
            if ('status' not in obj or obj['status'] is None):
                print(" status is null" )
                return
            if ('requestid' not in obj or obj['requestid'] is None):
                print(" requestid is null")
                return
            sql_con = 'status = %d ' %(obj['status'])
            print("**"*20,sql_con)
            if ('res_img' in obj and obj['res_img'] is not None):
                sql_con += ", res_img = '" + obj['res_img'] + "'"

            sql = "UPDATE " + self.dbname + " SET " + sql_con + " WHERE requestid = '%s'" %(obj['requestid'])
            print("update sql: ",sql)
            try:
                db.cursor.execute(sql)
                db.conn.commit()
                print("更新成功！！！")
            except Exception as e:
                db.conn.rollback()
                traceback.print_exc()


    def update_tasks(self, objs):
        with self as db:
            if len(objs) < 1:
                return
            sqls = ""
            for obj in objs:
                if ('status' not in obj or obj['status'] is None):
                    print(" status is null" )
                    continue
                if ('requestid' not in obj or obj['requestid'] is None):
                    print(" requestid is null")
                    continue
                # 使用cursor()方法获取操作游标
                sql_con = 'status = %d ' %(obj['status'])
                print("**"*20,sql_con)
                if ('res_img' in obj and obj['res_img'] is not None):
                    sql_con += ", res_img = '" + obj['res_img'] + "'"
                #print("@@"*20,sql_con)
                # SQL 更新语句
                sql = "UPDATE " + self.dbname + " SET " + sql_con + " WHERE requestid = '%s' ;" %(obj['requestid'])
                sqls += sql
            print("update sql: ",sqls)
            try:
                db.cursor.execute(sqls)
                db.conn.commit()
                print("更新成功！！！")
            except Exception as e:
                db.conn.rollback()
                traceback.print_exc()

    def __enter__(self):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()


sqlhelper = SqlHelper()
