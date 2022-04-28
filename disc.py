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


# 自分のBotのアクセストークンに置き換えてください
TOKEN = mizuho.settings["discToken"]

# 接続に必要なオブジェクトを生成
intents = discord.Intents.all()
client = discord.Client(intents=intents)

mode = 1

def setMode(x):
    global mode
    mode = x

async def speak(result):
    global channel
    pattern = re.compile(r"^!command")
    if bool(pattern.search(result)):
        com = result.split(" ")
        if com[1] == "discMove":
            if client.get_channel(int(com[2])) != None:
                channel = client.get_channel(int(com[2]))
            try:
                print("チャンネルを移動しました: {}".format(channel.name))
            except:
                print("チャンネルを移動しました: DM")
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


        if message.content == "mizuho!mode 0":
            await message.channel.send("沈黙モードに切り替える")
            setMode(0)
            return
        if message.content == "mizuho!mode 1":
            await message.channel.send("通常モードに切り替える")
            setMode(1)
            return

        print("受信: {}".format(message.content))
        lastMessage = message
        prevTime = time.time()
        mizuho.receive(message.content, message.author.name)
        if mode == 1:
            messages.append(message)



i = 0
@tasks.loop(seconds=6)
async def cron():
    try:
        global persons, prevTime, lastMessage, i, messages

        if len(messages) != 0:
            message = [messages[-1].content, messages[-1].author.name]
            messages = []
            result = mizuho.speakFreely(message[0], message[1])
            if result == None: return
            print("{}: {}".format(mizuho.settings["myname"], result))
            await speak(result)
        nowTime = time.time()
        if (nowTime - prevTime) >= 20 and random.randint(0, 100) >= 75:
            mizuho.receive("!command shut up", lastMessage.author.name)
            result = mizuho.speakFreely("!command shut up", lastMessage.author.name)
            if result == None: return
            print("{}: {}".format(mizuho.settings["myname"], result))
            prevTime = time.time()
            await speak(result)

    except:
        import traceback
        traceback.print_exc()


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
