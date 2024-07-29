import time

from utils.actions.prompt_to_image import *
from utils.actions.prompt_image_to_image import *
from utils.actions.load_workflow import load_workflow
from utils.helpers.qiniu_tool import *
from api.api_helpers import clear
import sys
import os
import pika
import json
import traceback
SERVER_HOST = os.environ.get('SERVER_HOST','http://47.116.76.13:5001/')
task_url = SERVER_HOST + "get_tasks"
update_task_url = SERVER_HOST + "update_task"
headers = {
    "Content-Type": "application/json"
}

def design(input_img_url, style_img_url,positve_prompt='',negative_prompt=''):
    img_list = []
    try:
        #download file
        input_img,style_img = get_input_file(input_img_url,style_img_url)
        # input_img = 'd35d33271d2c784838e4f54fe521028ed2d1e73f19aa1d-n7F3Gj.png',
        # style_img = 'ComfyUI_00173_.png'
        res_list = prompt_to_image_mmq(workflow, input_img=input_img, style_img=style_img,
                                       positve_prompt=positve_prompt, negative_prompt=negative_prompt,
                                       save_previews=True)
        img_list = upload_img_list(res_list)

        return img_list ,True
    except Exception as e:
        print(traceback.format_exc())
        print(f"An error occurred: {e}")
        exit_program()
        return [], False

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

def clear_comfy():
    clear(True, True)

def callbackFunctionForProcess(ch, method, properties, body):
    task = json.loads(body)
    rid = task.get('requestid', '')
    image = task.get('image', '')
    image2 = task.get('image2', '')
    model_param = task.get('model_param', '')
    cnt = task.get('cnt', 1)
    retry = task.get('retry', 0)
    if rid != '' and image != '' and image != "null":
        # 调用画图
        res_img_list,ok = design(image, image2, model_param)
        if ok:
            if len(res_img_list) > 0:
                task['status'] = 2
                task['res_img'] = ','.join(res_img_list)
                print("~~~~~~,res_img_list", task['res_img'])
            else:
                task['status'] = 1
        else:
            task['status'] = -1
        task['retry'] = retry + 1
        update_response = requests.request("POST", update_task_url, json=task, headers=headers)
        print("update_task:", update_response)

def start_task():
    credentials = pika.PlainCredentials(os.environ.get('MQ_NAME', 'wangyifan'),
                                        os.environ.get('MQ_PASS', 'dhYurts@7hh'))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.environ.get('MQ_HOST', '47.116.76.13'), port='5672', credentials=credentials, heartbeat=180))
    channel = connection.channel()
    channel.exchange_declare(os.environ.get('MQ_EXCHANGE', 'mmq_exchange'), durable=True, exchange_type='topic')
    channel.basic_consume(queue=os.environ.get('MQ_QUEUE', 'mmq'), on_message_callback=callbackFunctionForProcess,
                          auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    print("Welcome to the program!")
    workflow = load_workflow('./workflows/MMQ240517HD.json')
    start_task()
