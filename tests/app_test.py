# 消息队列rabbitmq-生产者
import pika



QUEUE_NAME = "mmq"
credentials = pika.PlainCredentials("wangyifan", "dhYurts@7hh")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='47.116.76.13', credentials=credentials))
channel = connection.channel()  # 频道对象 利用它可以操作队列内消息的生产和消费
channel.queue_declare(queue=QUEUE_NAME)  # 声明一个消息队列，队列名称为scrape


channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body='Hello,Rabbitmq!')  # 将数据存储到消