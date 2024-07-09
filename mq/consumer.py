#consumer
import pika
#declaring the credentials needed for connection like host, port, username, password, exchange etc
credentials = pika.PlainCredentials('wangyifan','dhYurts@7hh')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='47.116.76.13', port='5672', credentials= credentials))
channel = connection.channel()
channel.exchange_declare('mmq_exchange', durable=True, exchange_type='topic')
#defining callback functions responding to corresponding queue callbacks
def callbackFunctionForQueueA(ch,method,properties,body):
    print('Got a message from Queue A: ', body)
def callbackFunctionForQueueB(ch,method,properties,body):
    print('Got a message from Queue B: ', body)
def callbackFunctionForQueueC(ch,method,properties,body):
    print('Got a message from Queue C: ', body)
#Attaching consumer callback functions to respective queues that we wrote above
channel.basic_consume(queue='mmq', on_message_callback=callbackFunctionForQueueA, auto_ack=True)
channel.basic_consume(queue='B', on_message_callback=callbackFunctionForQueueB, auto_ack=True)
channel.basic_consume(queue='C', on_message_callback=callbackFunctionForQueueC, auto_ack=True)
#this will be command for starting the consumer session
channel.start_consuming()
