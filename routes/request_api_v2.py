
import pymysql
from flask import jsonify, abort, request, Blueprint
from dbtool.mysql_tool import MysqlTool
REQUEST_API = Blueprint('request_api_v2', __name__)
dbtool = MysqlTool()

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/v2/generate', methods=['POST'])
def generate():
    code = 200
    output = []
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    if not data.get('requestid'):
        abort(400)
    if not data.get('image'):
        abort(400)
    try:
        
        obj = dbtool.get_task_by_requestid(data.get('requestid'))
        print("obj:",obj)
        if (obj is None):
            new_task = {}
            new_task["requestid"] = data.get('requestid')
            new_task["image"] = data.get('image')
            new_task["normal_param"] = data.get('normal_param')
            new_task["control_param"] = data.get('control_param')
            ### 这里需要修改
            dbtool.create_task_v2(new_task)
            ## 这里可以暂停一下 比如10s
            tmp_obj = dbtool.get_task_by_requestid(data.get('requestid'))
            obj = tmp_obj

        if (obj["res_img2"] and len(obj["res_img2"]) >0):
                output = obj["res_img2"].split(',')
                msg = "生成成功"
        else:
            code = 100
            msg = "排队中"
    except Exception as e:
        print("失败啦",e)
        code = -1
        msg = "查询失败"

    res_data = {
        "code": code,
        "msg": msg,
        "data": output
    }

    # HTTP 201 Created
    return jsonify(res_data), 200

@REQUEST_API.route('/v2/get_task')
def get_task():
    msg = "查询成功"
    code = 200
    try:
        dbtool = MysqlTool(pool,DBNAME)
        task = dbtool.get_task_by_status(1)
        #print("/v2/get_task:", task)
        if task is None:
            #print("hhhhhhh")
            code = -1
            msg = "查询失败"
        else:
            #print("gggggggg"*50)
            task['status'] = 0
            dbtool.update_task(task)
    except:
        code = -1
        msg = "查询失败"
        task = None
    #print("*******",task)
    res_data = {
        "code": code,
        "msg": msg,
        "data": task
    }
    # HTTP 201 Created
    return jsonify(res_data), 200


@REQUEST_API.route('/v2/update_task', methods=['POST'])
def update_task():
    msg = "更新成功"
    code = 200
    if not request.get_json():
        abort(400)
    task = request.get_json(force=True)

    if not task.get('requestid'):
        abort(400)
    try:
        dbtool.update_task(task)
    except:
        code = -1
        msg = "更新失败"

    res_data = {
        "code": code,
        "msg": msg,
        "data":""
    }
    # HTTP 201 Created
    return jsonify(res_data), 200
