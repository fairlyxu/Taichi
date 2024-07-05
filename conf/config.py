# import os

# 基础配置，使用继承的方式
class BaseConfig:
    TESTING = False
    # MySQL所在主机名，默认127.0.0.1
    HOSTNAME = "127.0.0.1"
    # MySQL监听的端口号，默认3306
    PORT = 3306
    # 连接MySQL的用户名，自己设置
    USERNAME = "root"
    # 连接MySQL的密码，自己设置
    PASSWORD = "root"
    # MySQL上创建的数据库名称
    DATABASE = "database_learn"
    # 通过修改以下代码来操作不同的SQL比写原生SQL简单很多 --》通过ORM可以实现从底层更改使用的SQL
    # app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"


class DBConfig(BaseConfig):
    # 开启debug
    DEBUG = True

    # mysql配置
    HOSTNAME = "211.103.157.180"
    PORT = 3310
    USERNAME = "用户名"
    PASSWORD = "密码"
    DATABASE = "数据库名"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"


class ProductionConfig(BaseConfig):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

