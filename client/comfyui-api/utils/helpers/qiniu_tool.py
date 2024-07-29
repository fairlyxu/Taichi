
from qiniu import Auth, put_file
import uuid
import time
import os
import requests

DOMAIN_NAME = os.environ.get('DOMAIN_NAME')
BUCKED_NAME = os.environ.get('BUCKED_NAME')
ACC_KEY = os.environ.get('ACCE_KEY')
SECR_KEY = os.environ.get('SECR_KEY')
def upload_img(file_name):
    """
    """
    file_location = os.environ.get('OUTPUT_IMG_DIR','C:/') + file_name
    # 指定上传空间，获取token
    q = Auth(access_key=ACC_KEY, secret_key=SECR_KEY)
    token = q.upload_token(BUCKED_NAME)
    uuid_str = uuid.uuid4().hex
    dt = time.strftime("%Y%m%d-%H", time.localtime())
    tmp_file_name = '%s_%s.png' % (dt,uuid_str)
    ret, info = put_file(token, tmp_file_name,file_location)
    os.remove(file_location)
    if info.status_code == 200:
        img_url = DOMAIN_NAME + '/' + ret.get('key')
        return True, img_url
    else:
        return False, None

def upload_img_list(file_location_list):
    res = []
    for img in file_location_list:
        ret, info = upload_img(img)
        if ret:
            res.append("https://" + info)
    return res


def get_input_file(input_img_url,style_img_url):
    input_img = str(uuid.uuid4().hex) + ".jpg"
    style_img = str(uuid.uuid4().hex ) + ".jpg"
    download_image(input_img_url, os.environ.get('INPUT_IMG_DIR','C:/') + input_img)
    download_image(style_img_url, os.environ.get('INPUT_IMG_DIR','C:/') + style_img)
    return input_img,style_img

def download_image(url, save_file):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_file, 'wb') as out_file:
            out_file.write(response.content)
        print("Image successfully downloaded: ", save_file)
    else:
        print("Error: unable to download image, status code: ", response.status_code)


if __name__ == '__main__':
    res_list = ['../../output/ComfyUI_00364_.png']
    #img_list = upload_img_list(res_list)
    # 获得根路径

