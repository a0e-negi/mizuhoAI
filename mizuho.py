# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from difflib import SequenceMatcher


def common_seq(lhs, rhs):
    r"""
    >>> print("\n".join(common_seq("ABChhh", "XYZkkk")))
    <BLANKLINE>
    >>> print("\n".join(common_seq("ABChhh", "ABCkkk")))
    ABC
    >>> print("\n".join(common_seq("zzABChhh", "ABCkkk")))
    ABC
    >>> print("\n".join(common_seq("ABChhh", "yyABCkkk")))
    ABC
    >>> print("\n".join(common_seq("zzABChhh", "yyABCkkk")))
    ABC
    >>> print("\n".join(common_seq("uvwxABChhh", "yzABCkkk")))
    ABC
    >>> print("\n".join(common_seq("uvwABChhh", "xyzABCkkk")))
    ABC
    """
    sm = SequenceMatcher(a=lhs, b=rhs)
    return [lhs[slice(m.a, m.a + m.size)]
            for m in sm.get_matching_blocks() if m.size]




import re
import json
import random
import time

savefile = "mizuho.json"
with open(savefile, "r", encoding="utf8") as f:
    data = json.load(f)
heart = len(data["sentence"]) - 20
heartLastSpeaker = None

def looking(x):
    global heart, heartLastSpeaker
    try:
        i = heart
        for sen in data["sentence"][heart:-1]:
            into = x
            while True:
                pattern = re.compile(r"{}$".format(into))
                if 1 == len(into): 
                    break
                if bool(pattern.search(sen[0])):
                    if i+1 != len(data["sentence"]) and data["sentence"][i+1][1] != data["myname"]:
                        heart = i+1
                        heartLastSpeaker = data["sentence"][i+1][1]
                        return data["sentence"][i+1][0]
                    else:
                        ii = 0
                        while True:
                            if i+ii+1 != len(data["sentence"]) and data["sentence"][i+ii+1][1] != data["myname"]:
                                heart = i+ii+1
                                heartLastSpeaker = data["sentence"][i+ii+1][1]
                                return data["sentence"][i+ii+1][0]
                            ii += 1
                into = into[1:]
            if i >= 20:
                continue
            i += 1
    except:
        pass

    try:
        i = heart - 20
        for sen in data["sentence"][heart-20:-1]:
            into = x
            while True:
                pattern = re.compile(r"{}$".format(into))
                if 1 == len(into): 
                    break
                if bool(pattern.search(sen[0])):
                    if i+1 != len(data["sentence"]) and data["sentence"][i+1][1] != data["myname"]:
                        heart = i+1
                        heartLastSpeaker = data["sentence"][i+1][1]
                        return data["sentence"][i+1][0]
                    else:
                        ii = 0
                        while True:
                            if i+ii+1 != len(data["sentence"]) and data["sentence"][i+ii+1][1] != data["myname"]:
                                heart = i+ii+1
                                heartLastSpeaker = data["sentence"][i+ii+1][1]
                                return data["sentence"][i+ii+1][0]
                            ii += 1
                into = into[1:]
            if i >= 40:
                continue
            i += 1
    except:
        pass

    try:
        i = 0
        for sen in data["sentence"]:
            into = x
            while True:
                pattern = re.compile(r"{}$".format(into))
                if 1 == len(into): 
                    break
                if bool(pattern.search(sen[0])):
                    if i+1 != len(data["sentence"]) and data["sentence"][i+1][1] != data["myname"]:
                        heart = i+1
                        heartLastSpeaker = data["sentence"][i+1][1]
                        return data["sentence"][i+1][0]
                    else:
                        ii = 0
                        while True:
                            if i+ii+1 != len(data["sentence"]) and data["sentence"][i+ii+1][1] != data["myname"]:
                                heart = i+ii+1
                                heartLastSpeaker = data["sentence"][i+ii+1][1]
                                return data["sentence"][i+ii+1][0]
                            ii += 1
                into = into[1:]
            i += 1
    except:
        pass
    
    return data["sentence"][-1][0]

def tsuzuki():
    global heart
    i = 1
    try:
        while True:
            if data["sentence"][heart+i][1] == heartLastSpeaker:
                return data["sentence"][heart+i][0]
            i += 1
    except:
        pass

def addSentence(x, u):
    data["sentence"].append([x, u])

def save():
    global savefile
    with open(savefile, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

def speakFreely(x, u):
    result = looking(x).replace(data["myname"], u)
    addSentence(result, data["myname"])
    print("現在の心: {}".format(heart))
    print(heartLastSpeaker)
    return result

def receive(x, u):
    if x == "" or u == "": return
    addSentence(x, u)
    looking(x)



"""
while True:
    into = input("> ")
    receive(into, "ゆいな")
    print(speakFreely(into, "ゆいな"))
    save()
"""

persons = [data["myname"]]
channel = None
lastMessage = None
prevTime = time.time()

# インストールした discord.py を読み込む
from discord.ext import tasks
import discord
import threading
import asyncio


# 自分のBotのアクセストークンに置き換えてください
TOKEN = "トークン"

# 接続に必要なオブジェクトを生成
client = discord.Client()

async def speak(result):
    global channel
    pattern = re.compile(r"^!command")
    if bool(pattern.search(result)):
        com = split(" ")
        if com[1] == "discMove":
            channel = client.get_channel(com[2])
            print("チャンネルを移動しました: {}".format(channel.name))
    else:
        await channel.send(result)

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    cron.start()

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    global channel, persons, prevTime, lastMessage
    if message.channel == channel or data["myname"] in message.content:
        if message.channel != channel:
            print("チャンネルを移動しました: {}".format(message.channel.name))
            channel = message.channel
            receive("!command discMove {}".format(message.channel.id), message.author.name)
        if message.author == client.user:
            return
        if message.author.name not in persons:
            persons.append(message.author.name)
        if message.content == "":
            return
        
        print("受信: {}".format(message.content))
        prevTime = time.time()
        lastMessage = message
        if random.randint(1, len(persons) - 1) == len(persons) - 1 or data["myname"] in message.content:
            receive(message.content, message.author.name)
            result = speakFreely(message.content, message.author.name)
            print("みずほ: {}".format(result))
            time.sleep(4)
            await speak(result)
        else:
            receive(message.content, message.author.name)
        save()


i = 0
@tasks.loop(seconds=20)
async def cron():
    global persons, prevTime, lastMessage, i
    nowTime = time.time()
    if nowTime >= prevTime + 20:
        print("沈黙を検知")
        if i >= 3:
            persons = [data["myname"]]
            i = 0
        if channel != None or lastMessage != None:
            if random.randint(1, len(persons) *2) == len(persons) * 2:
                result = speakFreely(lastMessage.content, lastMessage.author.name)
                print("みずほ: {}".format(result))
                await tsuzuki()
        i += 1
        prevTime = time.time()



# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
