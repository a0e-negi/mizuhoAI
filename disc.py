import mizuho
import time
import random
import re
import sys
if sys.argv[1]:
    mizuho.initialize(sys.argv[1], "discord")
else:
    print("人格フォルダを指定してください。")
    exit()

persons = [mizuho.settings["myname"]]
channel = None
lastMessage = None
messages = []
prevTime = time.time()


from discord.ext import tasks
import discord
import threading
import asyncio
import random


# 自分のBotのアクセストークンに置き換えてください
TOKEN = mizuho.settings["discToken"]

# 接続に必要なオブジェクトを生成
intents = discord.Intents.all()
client = discord.Client(intents=intents)

mode = 2

def setMode(x):
    global mode, channel
    mode = x
    print("mode: {}".format(mode))

async def speak(result):
    global channel, persons
    pattern = re.compile(r"^!command")
    print("users: {}".format(persons))
    if bool(pattern.search(result)):
        com = result.split(" ")
        if com[1] == "discMove":
            if client.get_channel(int(com[2])) != None:
                channel = client.get_channel(int(com[2]))
                persons = [mizuho.settings["myname"]]
            try:
                print("チャンネルを移動しました: {}".format(channel.name))
            except:
                print("チャンネルを移動しました: DM")
        elif com[1] == "modeChange":
            setMode(int(com[2]))
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
    global channel, persons, prevTime, lastMessage, messages
    
    if message.channel == channel or bool(re.search(mizuho.settings["mynames"], message.content)) or isinstance(message.channel, discord.DMChannel):
        if message.channel != channel:
            try:
                print("チャンネルを移動しました: {}".format(message.channel.name))
            except:
                print("チャンネルを移動しました: {}のDM".format(message.author.name))
            channel = message.channel
            persons = [mizuho.settings["myname"]]
            mizuho.receive("!command discMove {}".format(message.channel.id), message.author.name)
        if message.author == client.user:
            return
        if message.author.name not in persons:
            persons.append(message.author.name)
        if message.content == "":
            return
        if message.content == None:
            return

        """
        if bool(re.search("沈黙モード|黙|だま", message.content)) and bool(re.search(mizuho.settings["mynames"], message.content)):
            mizuho.receive(message.content, message.author.name)
            setMode(0)
        """
        if bool(re.search("寡黙モード|静かに|しずかに", message.content)) and bool(re.search(mizuho.settings["mynames"], message.content)):
            mizuho.receive("!command modeChange 1", "_BRAIN_")
            setMode(1)
        if bool(re.search("通常モード|喋って|話して|しゃべって|はなして", message.content)) and bool(re.search(mizuho.settings["mynames"], message.content)):
            mizuho.receive("!command modeChange 2", "_BRAIN_")
            setMode(2)

        lastMessage = message
        prevTime = time.time()
        lastMessage = message

        if mode == 2 or mode == 1:
            messages.append(message)



i = 0
@tasks.loop(seconds=4)
async def cron():
    try:
        global persons, prevTime, lastMessage, i, messages, receive

        if mode == 2:
            if len(messages) != 0:
                print("受信: {}, from {}".format(messages[-1].content, messages[-1].author.name))
                mizuho.receive(messages[-1].content, messages[-1].author.name)
                if random.randint(0, len(persons)-2) == 0 or bool(re.search(mizuho.settings["mynames"], messages[-1].content)):
                    result = mizuho.speakFreely()
                    if result == None:
                        messages = []
                    else:
                        print("{}: {}".format(mizuho.settings["myname"], result))
                        await speak(result)
                        messages = []
                else:
                    messages = []
        elif mode == 1:
            if len(messages) != 0:
                print("受信: {}, from {}".format(messages[-1].content, messages[-1].author.name))
                mizuho.receive(messages[-1].content, messages[-1].author.name)
                if bool(re.search(mizuho.settings["mynames"], messages[-1].content)):
                    result = mizuho.speakFreely()
                    if result == None:
                        messages = []
                    else:
                        print("{}: {}".format(mizuho.settings["myname"], result))
                        await speak(result)
                        messages = []
                else:
                    messages = []
        

        nowTime = time.time()
        if nowTime >= prevTime + 20:
            print("沈黙を検知")
            if i >= 3:
                persons = [mizuho.settings["myname"]]
                i = 0
            if channel != None and lastMessage != None:
                if mode == 2:
                    if random.randint(0, len(persons)-1) == 0:
                        result = mizuho.tsuzuki()
                        print("{}: {}".format(mizuho.settings["myname"], result))
                        if result != None:
                            await speak(result)

                
            i += 1
            prevTime = time.time()
    except:
        import traceback
        traceback.print_exc()


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
