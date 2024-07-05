import os


# declaring the credentials needed for connection like host, port, username, password, exchange etc
credentials = pika.PlainCredentials('wangyifan', 'dhYurts@7hh')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='47.116.76.13', credentials=credentials))
channel = connection.channel()
channel.exchange_declare('test', durable=True, exchange_type='topic')
channel.queue_declare(queue='A')
channel.queue_bind(exchange='test', queue='A', routing_key='A')
channel.queue_declare(queue='B')
channel.queue_bind(exchange='test', queue='B', routing_key='B')
channel.queue_declare(queue='C')
channel.queue_bind(exchange='test', queue='C', routing_key='C')


class ServerBaseConfig:
    PORT = os.environ.get('PORT', 5002)

class MQConfig():
    HOSTNAME = os.environ.get('MQ_HOST', '127.0.0.1') #47.116.76.13
    USERNAME = os.environ.get('DB_NAME', 'root')
    PASSWORD = os.environ.get('DB_PASS', 'pass')
    EXCHANGE = os.environ.get('EXCHANGE', 'test')
    QUEUE = os.environ.get('QUEUE', 'mmq')

class DBConfig():
    HOSTNAME = os.environ.get('DB_HOST', '127.0.0.1')
    PORT = os.environ.get('DB_PORT', 3306)
    USERNAME = os.environ.get('DB_NAME', 'root')
    PASSWORD = os.environ.get('DB_PASS', 'pass')
    DATABASE = os.environ.get('DATABASE', 'AIGC_TASK_EXCHAGE')

SERVER_CONFIG = {
    "server_conf": ServerBaseConfig,
    "db_conf": DBConfig,
    "mq_conf":MQConfig
}

