import numpy as np
import Model

import chainer
from chainer import cuda, Function, gradient_check, Variable, optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

import json
import random
import threading
import time



import sys
import yaml
import re

args = sys.argv
settingFile = args[1]
with open(settingFile, "r", encoding="utf8") as file:
    settings = yaml.safe_load(file)
    mynames = settings["names"]
    token = settings["token"]
    db = settings["db"]
    


def getResponseSentence(model, sentencies):
    att = []
    for i in range(len(sentencies)):
        if sentencies[i] in avocab:
            wid = avocab[sentencies[i]]
            x_k = F.relu(model.embedx(np.array([wid], dtype=np.int32)))
            h = F.relu(model.H(x_k))
            att.append(h.data[0])
    x_k = F.relu(model.embedx(np.array([avocab['<eos>']], dtype=np.int32)))
    h = F.relu(model.H(x_k))
    att.append(h.data[0])
    w = F.relu(model.W(h))
    w2 = F.relu(model.W2(h))
    w3 = F.relu(model.W3(h))
    w4 = F.relu(model.W4(h))
    wid = np.argmax(F.softmax(model.W5(
        Variable(np.array([chainer.functions.concat([w.data[0], w2.data[0], w3.data[0], w4.data[0]], axis=0).data], dtype=np.float32))
    )).data[0])
    res = id2wd[wid]
    loop = 0
    while (wid != bvocab['<eos>']) and (loop <= 30):
        x_k = F.relu(model.embedy(np.array([wid], dtype=np.int32)))

        i = 0
        c = [[0]*model.k]
        for at in att:
            a = F.tanh(model.A(Variable(np.array([chainer.functions.concat([h.data[0], at], axis=0).data], dtype=np.float32))))
            a2 = F.softmax(model.A2(a))
            c += a2.data
        c = np.array(c, dtype=np.float32)
        
        h = F.relu(model.H2(Variable(np.array([chainer.functions.concat([x_k.data[0], c[0]], axis=0).data], dtype=np.float32))))
        w = F.relu(model.W(h))
        w2 = F.relu(model.W2(h))
        w3 = F.relu(model.W3(h))
        w4 = F.relu(model.W4(h))
        wid = np.argmax(F.softmax(model.W5(
            Variable(np.array([chainer.functions.concat([w.data[0], w2.data[0], w3.data[0], w4.data[0]], axis=0).data], dtype=np.float32))
        )).data[0])
        if wid in id2wd:
            res += id2wd[wid] 
        loop += 1
    return res





alines, blines, avocab, av, bvocab, bv, id2wd, extra = np.load("data.npy", allow_pickle=True)

demb = 500
model = Model.ConversationModel(av, bv, avocab, bvocab, demb)
serializers.load_npz(db, model)
optimizer = optimizers.Adam()
optimizer.setup(model)

#ここからメッセージ取得&返信


"""
import atexit
@atexit.register
def finallSyori():
    serializers.save_npz(db, model)
    print("セーブしました。")
"""


lastRes = "(BOS)"

while True:
    a = input("> ")

    if a == "":
        print("終了します。")
        exit()

    into = lastRes
    ex = a
    for epoch in range(1):
        isChanged = False


        model.cleargrads()
        print("{} => {}".format(into, ex))
        loss = model(into, ex)
        print(float(loss.data))
        loss.backward()
        loss.unchain_backward()
        optimizer.update()
        loss = model(into, ex)
        print(float(loss.data))
        print(epoch, " epoch finished.")

    lastRes = "{}: {}".format("笑いのユートピア", a)

    res = getResponseSentence(model, lastRes)
    lastRes = "{}: {}".format(mynames.split("|")[0], res)
    print(res)

