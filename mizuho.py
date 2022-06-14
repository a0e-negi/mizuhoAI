
import re
import json
import random
import time

import pandas as pd
from simpletransformers.t5 import T5Model, T5Args



settings = None #設定
direc = None #データのディレクトリ
interface = 0 #クライアントの種類
lastMessage = ["こんにちは", "笑いのユートピア"]
model = None

def initialize(direcectory, interface_):
    #初期化
    global settings, direc, interface, model
    direc = direcectory
    interface = interface_
    with open(direc+"/settings.json", "r", encoding="utf8") as f:
        settings = json.load(f)

    # Configure the model
    model_args = T5Args()
    model_args.num_train_epochs = 1
    model_args.overwrite_output_dir = True
    model_args.save_eval_checkpoints = False
    model_args.output_dir = direc+"/outputs"

    try:
        model = T5Model("t5", direc+"/outputs", args=model_args, use_cuda=False)
    except:
        model = T5Model("t5", "sonoisa/t5-base-japanese", args=model_args, use_cuda=False)

def receive(message, userName):
    global lastMessage, model, direc
    train_data = [
        ["receive message", "{}; {}".format(lastMessage[0], lastMessage[1]) , "{}".format(message)]
    ]
    train_df = pd.DataFrame(train_data)
    train_df.columns = ["prefix", "input_text", "target_text"]

    model.train_model(train_df, )
    lastMessage = [message, userName]

    to_predict = [
        "receive message: {}; {}".format(userName, message)
    ]
    result = model.predict(to_predict)[0]
    return result
    
def tsuzuki():
    global lastMessage, model
    to_predict = [
        "receive message: {}; {}".format(lastMessage[0], lastMessage[1])
    ]
    result = model.predict(to_predict)[0]
    return result




if __name__ == '__main__':
    import sys
    if sys.argv[1]:
        initialize(sys.argv[1], "bash")
    else:
        print("人格フォルダを指定してください。")
        exit()
    while True:
        into = input("> ")
        if into == "続き":
            print(tsuzuki())
        else:
            print("{}: {}".format(settings["myname"], receive(into, "笑いのユートピア")))
