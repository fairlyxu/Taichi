from utils.helpers.config import *
from utils.actions.prompt_to_image import *
from utils.actions.prompt_image_to_image import *
from utils.actions.load_workflow import load_workflow
from utils.helpers.qiniu_tool import *
from api.api_helpers import clear
import sys
import traceback
SERVER_HOST = os.environ.get('SERVER_HOST')
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
        input_img = 'd35d33271d2c784838e4f54fe521028ed2d1e73f19aa1d-n7F3Gj.png',
        style_img = 'ComfyUI_00173_.png'
        res_list = prompt_to_image_mmq(workflow, input_img=input_img, style_img=style_img,
                                       positve_prompt=positve_prompt, negative_prompt=negative_prompt,
                                       save_previews=True)
        img_list = upload_img_list(res_list)
    except Exception as e:
        print(traceback.format_exc())
        print(f"An error occurred: {e}")
        exit_program()

    return img_list

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

def clear_comfy():
    clear(True, True)

def task(num):
    while True:
        try:
            # time.sleep(2)
            task_request = requests.request("GET", task_url, headers=headers)
            response = json.loads(task_request.text)
            res = True
            if response["code"] == 200:
                tasks = response["data"]
                if tasks is not None and len(tasks) > 0:
                    for task in tasks:
                        rid = task.get('requestid','')
                        image = task.get('image','')
                        image2 = task.get('image2','')
                        model_param = task.get('model_param','')
                        cnt = task.get('cnt',1)
                        if rid != '' and image != '' and image != "null":
                            # 调用画图
                            res_img_list = design(image,image2,model_param)
                            if len(res_img_list) > 0:
                                # 上传七牛云并且更新数据库
                                if res:
                                    task['status'] = 2
                                    task['res_img'] = ','.join(res_img_list)
                                    print("~~~~~~,res_img_list",task['res_img'] )
                                else:
                                    task['status'] = 1
                                update_response = requests.request("POST", update_task_url, json=task, headers=headers)
                                print("update_task:", update_response)
                # print(num, "--->", res)
        except Exception:
            print(traceback.format_exc())

if __name__ == '__main__':
    print("Welcome to the program!")
    workflow = load_workflow('./workflows/MMQ240517HD.json')
    task()
