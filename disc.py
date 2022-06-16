import discord

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
        np.array([chainer.functions.concat([w.data[0], w2.data[0], w3.data[0], w4.data[0]], axis=0).data], dtype=np.float32)
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
            np.array([chainer.functions.concat([w.data[0], w2.data[0], w3.data[0], w4.data[0]], axis=0).data], dtype=np.float32)
        )).data[0])
        if wid in id2wd:
            res += id2wd[wid] 
        loop += 1
    return res





alines, blines, avocab, av, bvocab, bv, id2wd, extra = np.load("data.npy", allow_pickle=True)

demb = 100
model = Model.ConversationModel(av, bv, avocab, bvocab, demb)
serializers.load_npz(db, model)
optimizer = optimizers.Adam()
optimizer.setup(model)

#ここからメッセージ取得&返信

#
#
#以下、discord処理
#
#

intents = discord.Intents.all()
client = discord.Client(intents=intents)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


lastRes = "(Begin) "
channel = False
member = [mynames.split("|")[0]]
mode = 0

import atexit
@atexit.register
def finallSyori():
    serializers.save_npz(db, model)
    time.sleep(5)
    print("セーブしました。")


@client.event
async def on_message(message):
    global lastRes, model, alines, blines, avocab, av, bvocab, bv, id2wd, channel, member, mode
    if client.user != message.author:

        if "mizuho!silent" == message.content:
            mode = 1
            await speak("サイレントモードに切り替える")
        elif "mizuho!addEL:" in message.content:
            command = message.content.split(":\n")
            flag = 0
            for ext in extra:
                if ext[0] == command[1]: flag = 1
            for ext in extra:
                if ext[1] == command[2]: flag = 1
            if flag == 0:
                extra.append([command[1], command[2]])
            np.save("data.npy", (alines, blines, avocab, av, bvocab, bv, id2wd, extra))
            await speak("追加文字を学習しました。")

        elif "mizuho!save" == message.content:
            serializers.save_npz(db, model)
            await speak("セーブしました。")
        
        elif "mizuho!train" in message.content:
            a = message.content.split(":\n")
            await speak("学習します: {}, {}".format(a[1], a[2]))
            
            into = a[1]
            ex = a[2]

            for epoch in range(3):
                isChanged = False

                print("into:{} ex:{}".format(into, ex))
                model.cleargrads()
                loss = model(into, ex)
                loss.backward()
                loss.unchain_backward()
                optimizer.update()
                print(epoch, " epoch finished.")


            await speak("学習しました。")

        elif "mizuho!help" == message.content:
            await speak("準備中です。")
        elif "mizuho!normal" == message.content:
            mode = 0
            await speak("ノーマルモードに切り替える")
        elif bool(re.search(mynames, message.content)) or message.channel == channel  or isinstance(message.channel, discord.DMChannel):
            if message.channel != channel:
                member = [mynames.split("|")[0]]
                channel = message.channel
                into = lastRes
                ex = "!cd dcm {}".format(channel.id)
                for epoch in range(1):
                    model.cleargrads()
                    print("into:{} ex:{}".format(into, ex))
                    loss = model(into, ex)
                    print(float(loss.data))
                    loss.backward()
                    loss.unchain_backward()
                    optimizer.update()
            if message.author.name not in member:
                member.append(message.author.name)

            if message.content == "" or message.content == False or message.content == None:
                return

            into = lastRes
            ex = message.content
            if len(message.content) <= 300:
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

            lastRes = "{}: {}".format(message.author.name, message.content)

            r = random.randint(1, len(member))
            l = len(member)
            print("{} == {}".format(r,l))
            if r == l or re.search(mynames, lastRes):
                res = getResponseSentence(model, lastRes)
                for ext in extra:
                    res = res.replace(ext[1], ext[0])
                if mode != 1: 
                    lastRes = "{}: {}".format(mynames.split("|")[0], res)
                    await speak(res)
            
            print("member: {}".format(member))



async def speak(x):
    global channel
    if re.match(r'!cd (.*?)', x):
        if re.match(r'!cd dcm (.*?)', x):
            match = re.search(r'\d+', x)
            channel = client.get_channel(int(match.group()))
            print("チャンネルを移動しました")
    else:
        await channel.send(x)



client.run(token)