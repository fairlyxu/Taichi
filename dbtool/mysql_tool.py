# 导入pymysql模块import pymysql
import traceback
import pymysql
from dbtool.db_pool import pool
class MysqlTool:
    # 初始化变量
    def __init__(self):
        # 创建数据库连接
        self.connect = pool.connection()
        self.cursor = self.connect.cursor()
        self.dbname = pool.database

    # 查询数据库的版本
    def find_version(self):
        self.cursor.execute("SELECT VERSION()")
        # 使用 fetchone() 方法获取单条数据.
        data = self.cursor.fetchone()
        print("Database version : %s " % data)

    def __close__(self):
        """
        A method used to close connection of mysql.
        :param conn:
        :param cursor:
        :return:
        """
        self.cursor.close()
        self.connect.close()

    # 数据库的查询操作
    def get_task_by_requestid(self, requestid):
        # 使用cursor()方法获取操作游标
        cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute("select * from %s where requestid='%s'" %(self.dbname,requestid))
            print("get_task_by_requestid 查询成功！！！！")
            return cursor.fetchall()[0]
        except:
            # 如果发生错误则回滚
            self.connect.rollback()

        self.__close__()

    # 数据库的查询操作
    def get_task_by_status(self, status,num=5):
        # 使用cursor()方法获取操作游标
        cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            sql= "select * from %s where status=%d limit %d" % (self.dbname, status,num)
            #print("###"*10,sql)
            cursor.execute(sql)
            res = cursor.fetchall()
            #print("get_task_by_status 查询成功！！！！", res)
            if res:
                return res
        except Exception as e:
            traceback.print_exc()
            print("get_task_by_status error~:", e)

        self.__close__()


    def create_task(self, obj):
        # 使用cursor()方法获取操作游标
        cursor = self.connect.cursor()

        # SQL 插入语句
        sql = """INSERT INTO %s (requestid,image,image2, model_param,cnt,status)
                    VALUES('%s','%s','%s','%s',%d,1)""" % (self.dbname, obj['requestid'], obj['image'], obj['image2'], obj['model_param'],obj['cnt'])
        #print(sql)
        try:
            cursor.execute(sql)
            self.connect.commit()
        except:
            self.connect.rollback()

        self.__close__()
        print("插入成功！！！！")

    # 数据库更新操作
    def update_task(self, obj):
        print("sql update_task :",obj)
        if ('status' not in obj or obj['status'] is None):
            print(" status is null" )
            return
        if ('requestid' not in obj or obj['requestid'] is None):
            print(" requestid is null")
            return
        # 使用cursor()方法获取操作游标
        cursor = self.connect.cursor()
        sql_con = 'status = %d ' %(obj['status'])
        print("**"*20,sql_con)
        if ('res_img' in obj and obj['res_img'] is not None):
            sql_con += ", res_img = '" + obj['res_img'] + "'"

        #print("@@"*20,sql_con)
        # SQL 更新语句
        sql = "UPDATE " + self.dbname + " SET " + sql_con + " WHERE requestid = '%s'" %(obj['requestid'])
        print("update sql: ",sql)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.connect.commit()
        except:
            # 发生错误时回滚
            self.connect.rollback()
        print("更新成功！！！")


    def update_tasks(self, objs):
        if len(objs) < 1:
            return
        sqls = ""
        cursor = self.connect.cursor()
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
            cursor.execute(sqls)
            self.connect.commit()
        except:
            self.connect.rollback()
        print("更新成功！！！")

    # 关闭数据库的提示信息
    def close_connect(self):
        # 关闭数据库连接
        self.connect.close()
        print("MySQL connection closed.")


if __name__ == "__main__":
    # 定义变量
    try:
        obj = {'requestid': '1234567ddd', 'image': 'https://img2.baidu.com/it/u=4251773486,3026766425&fm=253&app=138&size=w931&n=0&f=JPEG&fmt=auto?sec=1680454800&t=97c57b5295b3a0bb8ae66e95e4e442d3', 'prompt': 'a modern bedroom', 'a_prompt': 'best quality, extremely detailed, photo from Pinterest, interior, cinematic photo, ultra-detailed, ultra-realistic, award-winning', 'n_prompt': 'longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality'}
        db = MysqlTool()
        print("MySQL connection finished.")
        db.find_version()
        db.create_task(obj)
    except Exception as e:
        print("Error connecting to MySQL: " + str(e))
    except pymysql.err.OperationalError as e:
        print("连接意外断开、 数据库名未找到: " + str(e))

