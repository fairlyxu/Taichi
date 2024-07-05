# producer
import pika
from conf.server_config import SERVER_CONFIG

class Producer:
    def __init__(self):
        self.exchange = SERVER_CONFIG.MQConfig.EXCHANGE
        self.queue = SERVER_CONFIG.MQConfig.QUEUE

        self.connection = pika.BlockingConnection()
        # declaring the credentials needed for connection like host, port, username, password, exchange etc
        credentials = pika.PlainCredentials(SERVER_CONFIG.MQConfig.USERNAME, SERVER_CONFIG.MQConfig.PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=SERVER_CONFIG.MQConfig.HOSTNAME, credentials=credentials))
        self.channel = connection.channel()

    def run(self,message):
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.queue, body=message)
