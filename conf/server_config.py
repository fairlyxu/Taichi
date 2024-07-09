import os

class ServerBaseConfig:
    PORT = int(os.environ.get('PORT', 5002))

class MQConfig:
    HOSTNAME = os.environ.get('MQ_HOST', '127.0.0.1') #47.116.76.13
    USERNAME = os.environ.get('MQ_NAME', 'root')
    PASSWORD = os.environ.get('MQ_PASS', 'pass')
    EXCHANGE = os.environ.get('MQ_EXCHANGE', 'test')
    QUEUE = os.environ.get('MQ_QUEUE', 'mmq')

class DBConfig:
    HOSTNAME = os.environ.get('DB_HOST', '127.0.0.1')
    PORT = int(os.environ.get('DB_PORT', 3306))
    USERNAME = os.environ.get('DB_NAME', 'root')
    PASSWORD = os.environ.get('DB_PASS', 'pass')
    DATABASE = os.environ.get('DATABASE', 'AIGC_TASK')


serverBaseConfig=ServerBaseConfig()
dbConfig=DBConfig()
mqConfig=MQConfig()
SERVER_CONFIG = {
    "BASICConf": serverBaseConfig,
    "DBConfig": dbConfig,
    "MQConfig": mqConfig
}

