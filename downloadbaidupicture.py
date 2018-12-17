#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/15 20:26
# @Author  : MxRanger
# @Site    : 
# @File    : downloadbaidupicture.py
# @Software: PyCharm



import requests
import json
import os
import random

class BaiDuPicture:
    def __init__(self,keyword):
        self.keyword = keyword
        self.url = "https://image.baidu.com/search/acjson"
        self.header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
                       "Referer" : "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E9%9B%BE%E5%A4%A9"
                       }

        #代理ip池
        self.proxies_list = [
            {"http": "123.57.76.102:80"},
            {"http":"61.135.217.7"},
            {"http":"118.78.196.19"},
            {"http":"115.223.121.94"},
            {"http":"47.96.148.248"},
            {"http":"47.95.9.128"},
            {"http":"115.223.207.144"},
            {"http":"118.24.61.165"},
            {"http":"47.95.9.128"},
            {"http":"219.141.153.12"},
            {"http":"120.79.7.88"},
            {"http":"117.191.11.110"},

        ]

    def getRandomProxy(self):
        return random.choice(self.proxies_list)

    #准备所需参数
    def getParams(self,page):
        return {'tn': 'resultjson_com',
                       'ipn': 'rj',
                       'ct': 201326592,
                       'is': '',
                       'fp': 'result',
                       'queryWord': self.keyword,
                       'cl': 2,
                       'lm': -1,
                       'ie': 'utf-8',
                       'oe': 'utf-8',
                       'adpicid': '',
                       'st': -1,
                       'z': '',
                       'ic': 0,
                       'word': self.keyword,
                       's': '',
                       'se': '',
                       'tab': '',
                       'width': '',
                       'height': '',
                       'face': 0,
                       'istype': 2,
                       'qc': '',
                       'nc': 1,
                       'fr': '',
                       'pn': page,
                       'rn': 30,
                       'gsm': '1e',
                       '1544876412197': ''}

    #解析url
    def parseUrl(self,page):
        params = self.getParams(page=page)
        response = requests.get(url=self.url,params=params,proxies=self.getRandomProxy())
        return response.content.decode()

    #保存响应json
    def saveJson(self,result_json,number):
        with open("result"+str(number)+".json", "w", encoding="utf-8") as f:
            f.write(result_json)

    #保存图片url
    def saveImageUrl(self,result_json,number):

        # [3] json.loads把json字符串转化为python类型
        result_json = json.loads(result_json)

        if not os.path.exists("./urltxt/"):
            os.makedirs("./urltxt/")

        # 创建目录
        if not os.path.exists("./urltxt/" + self.keyword):
            os.makedirs("./urltxt/" + self.keyword)

        with open("./urltxt/" + self.keyword+"/picture"+str(number)+".txt", "w", encoding="utf-8") as f:
            for i in result_json["data"]:
                if len(i) != 0:
                    if i["hoverURL"] != "":
                        f.write(i["hoverURL"] + "\n")
                    elif i["middleURL"] != "":
                        f.write(i["middleURL"] + "\n")
                    elif i["thumbURL"] != "":
                        f.write(i["thumbURL"] + "\n")

    #读取文件，下载图片
    def readAndDownload(self,number):
        flag = 0
        with open("./urltxt/" + self.keyword+"/picture"+str(number)+".txt", "r", encoding="utf-8") as f:
            line = f.readline()
            while line:
                flag += 1
                print(line)

                # 创建目录
                if not os.path.exists("./picture/"+self.keyword):
                    os.makedirs("./picture/"+self.keyword)

                # 下载图片
                img_res = requests.get(url=line,proxies=self.getRandomProxy())
                with open("./picture/"+self.keyword+"/img"+str(number)+"_" + str(flag) + ".jpg", "wb") as img_f:
                    img_f.write(img_res.content)

                # 游标向下继续
                line = f.readline()


if __name__ == '__main__':
    baidu = BaiDuPicture("雾天风景")

    batch_size = 40
    for index in range(batch_size):
        i = index + 1
        # [1] 一个批次
        result_json = baidu.parseUrl(30*i)
        # [2] 保存json
        #baidu.saveJson(result_json,i)
        # [4] 保存每一批次的图片url
        baidu.saveImageUrl(result_json,i)
        # [5] 读取图片url
        baidu.readAndDownload(i)


