import http.client
import json
import time

conn = http.client.HTTPConnection("47.116.76.13:5001")

json_data = {
	"requestid": "8eaaaaadddssssdddd",
	"image": "https://qiniu.aigcute.com/photography_ai/20240722/03a0e4ecd80b41849757bee86e46b00c.jpeg",
	"image2": "https://qiniu.aigcute.com/photography_ai/20240516/c04931b0cb99498c86b9034476db8381.png",
	"cnt": 1,
	"model_param": {},
	"custom_param":{}}
headers = {
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate, br",
    'User-Agent': "PostmanRuntime-ApipostRuntime/1.1.0",
    'Connection': "keep-alive",
    'Content-Type': "application/json"
    }

i = 0
while True:
    json_data["requestid"] = "s" + str(i)
    payload = json.dumps(json_data)
    conn.request("POST", "/generate", payload, headers)
    res = conn.getresponse()
    data = res.read()

    time.sleep(10)
    i+=1

    print(data.decode("utf-8"))