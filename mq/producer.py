import time
import pika
import traceback

class Producer:
    def __init__(self):
        self.exchange = 'mmq_exchange'
        self.queue = 'mmq'
        self.host = '47.116.76.13'
        self.credentials = pika.PlainCredentials("wangyifan", "dhYurts@7hh")
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        """建立RabbitMQ连接和频道"""
        if self.connection is not None:
            try:
                self.connection.close()
            except :
                traceback.print_exc()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                credentials=self.credentials,
                heartbeat=600,
                connection_attempts=5,
                retry_delay=2
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def run(self, message):
        """发送消息，如果连接断开则尝试重连"""
        try:
            print("~~~producer start~~~", message)
            print(self.exchange, self.queue)
            self.channel.basic_publish(exchange='', routing_key=self.queue, body=message)
        except pika.exceptions.ConnectionClosed:
            print("Connection was closed, re-establishing connection and retrying...")
            self.connect()
            self.run(message)

producer = Producer()
