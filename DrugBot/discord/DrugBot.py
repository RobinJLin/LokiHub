#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = "lanlanlu"
__contact__ = "xww1748.fl06@g2.nctu.edu.tw"

"""
    Loki 2.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No Match Intent!"
                }
            ]
        }
"""

import requests
import logging
logging.basicConfig(level=logging.CRITICAL) # 檢查Bug

try:
    from intent import Loki_character
    from intent import Loki_color
    from intent import Loki_number
    from intent import Loki_shape
except:
    from .intent import Loki_character
    from .intent import Loki_color
    from .intent import Loki_number
    from .intent import Loki_shape


LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = ""
LOKI_KEY = ""
# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []

        try:
            result = requests.post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": INTENT_FILTER
            },verify=False)

            if result.status_code == requests.codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "Connect failed."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

# 把字串全形轉半形 (繁體中文的語音輸入會自動讓英文變全形)
def strQ2B(s):
    rstring = ""
    for uchar in s:
        u_code = ord(uchar) # ord()拿到ASCII code
        if u_code == 12288:  # 全形空格直接轉換
            u_code = 32
        elif 65313 <= u_code <= 65338:  # 全形A~Z
            u_code -= 65248
        rstring += chr(u_code)
    if rstring == "":
        return s
    return rstring

def runLoki(inputLIST):
    logging.debug("runLoki in")
    resultDICT = {}
    resultDICT["color"]={}
    resultDICT["shape"]={}
    resultDICT["character"]={}
    resultDICT["number"]={}
    lokiRst = LokiResult(inputLIST)
    if lokiRst.getStatus():
        logging.debug("2")
        for index, key in enumerate(inputLIST):
            logging.debug("3")
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # character
                if lokiRst.getIntent(index, resultIndex) == "character":
                    resultDICT = Loki_character.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)
                    print("character: ",resultDICT["character"])
                    
                # color
                if lokiRst.getIntent(index, resultIndex) == "color":
                    resultDICT = Loki_color.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)
                    print("color: ",resultDICT["color"])

                # number
                if lokiRst.getIntent(index, resultIndex) == "number":
                    resultDICT = Loki_number.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)
                    print("number: ",resultDICT["number"])

                # shape
                if lokiRst.getIntent(index, resultIndex) == "shape":
                    resultDICT = Loki_shape.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)
                    print("shape: ",resultDICT["shape"])
                    
        sumLIST = [] # 用來集合對到的intent
        if (resultDICT["color"]!={}):
            sumLIST.append(resultDICT["color"])
        if (resultDICT["shape"]!={}):
            if resultDICT["shape"] == "藥":
                resultDICT["shape"] = "藥丸"
            elif resultDICT["shape"] == "藥水":
                resultDICT["shape"] = "液"
            elif resultDICT["shape"] == "藥錠":
                resultDICT["shape"] = "錠"
            sumLIST.append(resultDICT["shape"])
        if (resultDICT["character"]!={}):
            sumLIST.append(strQ2B(resultDICT["character"]))
        if(resultDICT["number"]!={}):
            sumLIST.append(resultDICT["number"])
            
        url = "https://drugs.olc.tw/drugs/outward/" + "%20".join(sumLIST) # 用join把sum裡面抓到的值 (intent) 插入sep (%20)
        #url = "https://drugs.olc.tw/drugs/outward/{}%20{}%20{}%20{}".format(resultDICT["color"],resultDICT["shape"], resultDICT["character"], resultDICT["number"])
    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return url


# 測試用
if __name__ == "__main__":
    inputLIST = ["我的狗狗好可愛"] # 白色圓形藥丸，上面寫SMT
    resultDICT = runLoki(inputLIST)
    print("Result => {}".format(resultDICT))
    
#    url = "https://drugs.olc.tw/drugs/outward/{} {}".format(resultDICT["color"],resultDICT["shape"])
#    response = requests.get(url)
#    print(url)
#    with open("drug.html","w",encoding="utf-8") as f:
#        f.write(response.text)
