#consumer
import pika
#declaring the credentials needed for connection like host, port, username, password, exchange etc
credentials = pika.PlainCredentials('wangyifan','dhYurts@7hh')

QUEUE_NAME = "mmq"
connection = pika.BlockingConnection(pika.ConnectionParameters(host='47.116.76.13', port='5672', credentials= credentials))

channel = connection.channel()  # 频道对象 利用它可以操作队列内消息的生产和消费
channel.queue_declare(queue=QUEUE_NAME)  # 声明一个消息队列，队列名称为scrape


# 从队列获取数据
def getData(ch, method, properties, body):
    print(f"得到{body}")


channel.basic_consume(queue=QUEUE_NAME, auto_ack=True, on_message_callback=getData)  # 从消息队列中取出数据，用到basic_consume
channel.start_consuming()