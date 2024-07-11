# producer
import time

import pika
from conf.server_config import SERVER_CONFIG

class Producer:
    def __init__(self):
        self.exchange = 'mmq_exchange'#SERVER_CONFIG['MQConfig'].EXCHANGE
        self.queue ='mmq'# SERVER_CONFIG['MQConfig'].QUEUE

        # declaring the credentials needed for connection like host, port, username, password, exchange etc
        credentials = pika.PlainCredentials("wangyifan", "dhYurts@7hh")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='47.116.76.13', credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)


    def run(self,message):
        print("~~~producer start~~~", message)
        print(self.exchange,self.queue)
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=message)

producer = Producer()
i=0

import json
while True:
    i+=1
    new_task = {}
    new_task["requestid"] = 'requestid= ' + str(i )
    new_task["image"] = 'image'
    new_task["image2"] = 'image2'
    new_task["cnt"] = 1
    new_task["model_param"] = 'model_param'
    obj_str = json.dumps(new_task)
    producer.run(obj_str)
    time.sleep(10)



