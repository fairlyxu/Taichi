
import traceback
import json
import g as G
from flask import jsonify, abort, request, Blueprint

REQUEST_API = Blueprint('request_api', __name__)
def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API

@REQUEST_API.route('/generate', methods=['POST'])
def generate():
    output = []
    code = 100
    msg = "排队中"
    cnt = 1
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    if not data.get('requestid'):
        abort(400)
    if not data.get('image'):
        abort(400)
    if data.get('cnt'):
        cnt = int(data.get('cnt'))

    try:
        #requestid,image,image2, model_param,cnt,status
        obj = G.dbtool.get_task_by_requestid(data.get('requestid'))
        print("obj:",obj)
        if (obj is None):
            new_task = {}
            new_task["requestid"] = data.get('requestid')
            new_task["image"] = data.get('image')
            new_task["image2"] = data.get('image2')
            new_task["cnt"] = cnt
            new_task["model_param"] = data.get('model_param')
            G.dbtool.create_task(new_task)
            #并且往消息队列中塞一条通知
            obj_str = json.dumps(new_task)
            print(obj)
            G.producer.run(message=obj_str)
        else:
            tmp_obj = G.dbtool.get_task_by_requestid(data.get('requestid'))
            obj = tmp_obj
            if (obj["res_img"] and len(obj["res_img"]) >0):
                output = obj["res_img"].split(',')
                msg = "生成成功"
                code = 200
    except :
        traceback.format_exc()
        code = -1
        msg = "查询失败"

    res_data = {
        "code": code,
        "msg": msg,
        "data": output
    }

    # HTTP 201 Created
    return jsonify(res_data), 200

@REQUEST_API.route('/get_tasks', methods=['GET'])
def get_task():
    msg = "查询成功"
    code = 200
    tasks = []
    try:
        #dbtool = MysqlTool(pool,DBNAME)
        tasks = G.dbtool.get_task_by_status(1) #[]
        #print("/v2/get_task:", task)
        if tasks is None:
            code = -1
            msg = "没有任务"
        else:
            for task in tasks:
                task['status'] = 0
            G.dbtool.update_tasks(tasks)
    except Exception:
        traceback.format_exc()
        code = -1
        msg = "查询失败"

    res_data = {
        "code": code,
        "msg": msg,
        "data": tasks
    }
    # HTTP 201 Created
    return jsonify(res_data), 200


@REQUEST_API.route('/update_task', methods=['POST'])
def update_task():
    msg = "更新成功"
    code = 200
    if not request.get_json():
        abort(400)
    task = request.get_json(force=True)
    if not task.get('requestid'):
        abort(400)
    try:
        G.dbtool.update_task(task)
    except:
        traceback.format_exc()
        code = -1
        msg = "更新失败"

    res_data = {
        "code": code,
        "msg": msg
    }
    # HTTP 201 Created
    return jsonify(res_data), 200
