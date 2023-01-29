#  @Author:     AlanStar
#  @Contact:    alan233@vip.qq.com
#  @License:    MIT
#  Copyright (c) 2022-2022

import json
import requests
from requests import Request, Session
from urllib3 import encode_multipart_formdata
from Core import config_loader as conf_load
from pathlib import Path

DODO_CLIENTID = conf_load.config.get("dodo_clientId", "")
DODO_TOKEN = conf_load.config.get("dodo_token", "")
DODO_CHANNEL = conf_load.config.get("dodo_channel", "")

# 拼接 Authorization 以组合公共请求头 -> ./Public_Headers.py
def combine_Authorization():
    Authorization = "Bot " + DODO_CLIENTID + "." + DODO_TOKEN
    return Authorization

# 公共请求头, 机器人的每次对API的请求都需要添加
Headers = {
    "Content-Type": "application/json",
    "Authorization": combine_Authorization()
}

# TODO: 频道消息支持Markdown
# 官方文档要求入参 referencedMessageId, 但无用法
# messageType  1: 文字信息  2: 图片信息  3: 视频信息  6: 卡片消息

# 文字消息
def send_text(channelId, content):
    # 预定义 URL 和 公共头
    URL = "https://botopen.imdodo.com/api/v2/channel/message/send"
    public_headers = Headers
    textData = {
        "channelId": channelId,
        "messageType": 1,
        "messageBody": {
            "content": content
        }
    }

    # 发送请求及 json 格式化处理
    message_info = requests.post(URL, headers=public_headers, data=json.dumps(textData))
    message_info = message_info.text
    message_info = json.loads(message_info)

    # 数据解析
    status = str(message_info["status"])
    status_message = message_info["message"]

    # 信息ID
    messageId = message_info["data"]["messageId"]

    # 打印信息ID
    print("\033[92m[Info]\033[0m 信息已发送", messageId)

    # 返回 json
    return message_info

# 图片消息
def send_pic(channelId, pic_url, width, height):
    URL = "https://botopen.imdodo.com/api/v2/channel/message/send"
    public_headers = Headers
    textData = {
        "channelId": channelId,
        "messageType": 2,
        "messageBody": {
            "url": pic_url,
            "width": width,
            "height": height,
            "isOriginal": 1
        }
    }

    # 发送请求及 json 格式化处理
    message_info = requests.post(URL, headers=public_headers, data=json.dumps(textData))
    message_info = message_info.text
    message_info = json.loads(message_info)

    # 数据解析
    status = str(message_info["status"])
    status_message = message_info["message"]

    # 信息ID
    messageId = message_info["data"]["messageId"]

    # 打印信息ID
    print("\033[92m[Info]\033[0m 信息已发送", messageId)

    # 返回 json
    return message_info

def pic_upload(filePath, fileName):
    URL = "https://botopen.imdodo.com/api/v2/resource/picture/upload"
    # 重新指定请求头, 此处不使用 PublicHeaders.py
    file_data = {
        "file": (fileName, open(filePath, "rb").read())
    }
    # 编码 multipart-data
    encode_data = encode_multipart_formdata(file_data)
    data = encode_data[0]
    # 重构请求头
    public_headers = {
        "Content-Type": encode_data[1],
        "Authorization": combine_Authorization()
    }
    # 调试用
    # print(public_headers)
    # print(filePath)

    # 生成请求体, 通过 session 请求,
    s = Session()
    req = Request("POST", url=URL, headers=public_headers, data=data)
    # 预计算请求头中的 Content-Length
    prepped = req.prepare()
    # 调试用
    # print(prepped.headers)
    # 使用 session 发送请求
    file_message = s.send(prepped)

    # 接受返回信息并转为 json
    file_message = file_message.text
    file_message = json.loads(file_message)

    # 数据解析
    status = file_message["status"]
    message = file_message["message"]

    # 返回 json
    return file_message

def send_password(raid_pokemon, extra_info, log):
    log.insert_text("Sending password to dodo channel...\n")
    # 上传图片
    result = pic_upload(Path("Autoraid.Windows/Core/image.jpg"), "image.jpg")
    # 发消息
    log.insert_text("upload result:" + result["status"] + " " + result["message"])
    log.insert_text(send_pic(channelId=DODO_CHANNEL, pic_url=result["data"]["url"], width=result["data"]["width"], height=result["data"]["height"]))

def send_finished(raid_pokemon, message):
    send_text(DODO_CHANNEL, "完成宝可梦" + raid_pokemon + "狩猎," +message)

if __name__ == "__main__":
    channelId = int(DODO_CHANNEL)
    textMessage = "Hello World"
    fileName = "snapshot.jpg"
    
    # 发文字
    # print(send_text(channelId=channelId, content=textMessage))
    # 发图片
    # print(send_pic(channelId=channelId, pic_url=pic_url, width=500, height=500))
    # 上传图片并发送
    result = pic_upload(fileName, fileName)
    print(result["status"], result["message"])
    print(send_pic(channelId=channelId, pic_url=result["data"]["url"], width=result["data"]["width"], height=result["data"]["height"]))