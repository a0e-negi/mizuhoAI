
import re
import json
import random
import time



data = None #別途読み込むデータ
settings = None #設定
direc = None #辞書のディレクトリ
actualUser = [] #今話してる人
brainUser = [] #過去に似た話をしてたユーザー
wordMemory = ["None"]*5 #重要な単語
heart = None #今の気持ち(ログの座標で表される)
replaceWords = True #単語を置き換えるか
lastSentence = None #最後のbotの言葉
lastSentenceInput = None #最後に聞いた言葉
heartLastSpeaker = None #過去に似た話をしてたユーザー
maeheart = 0 #一つ前の気持ち
interface = 0 #クライアントの種類
lastUser = None #最後に話しかけたユーザー
myVoice = None #心の中の声

def initialize(direcectory, interface_):
    #初期化
    global data, settings, direc, heart, interface
    direc = direcectory
    interface = interface_
    try:
        with open(direc+"/data.json", "r", encoding="utf8") as f:
            data = json.load(f)
        with open(direc+"/settings.json", "r", encoding="utf8") as f:
            settings = json.load(f)
    except:
        with open(direc+"/data_backup.json", "r", encoding="utf8") as f:
            data = json.load(f)
        with open(direc+"/settings.json", "r", encoding="utf8") as f:
            settings = json.load(f)
        with open(direc+"/data.json", "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    heart = len(data["sentence"]) - 50
    with open(direc+"/data_backup.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

def load():
    #データを読み込む
    global data, direc
    with open(direc+"/data.json", "r", encoding="utf8") as f:
        data = json.load(f)
    with open(direc+"/data_backup.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def looking(x, reply=True):
    #過去の発言をもとに考える
    global heart, heartLastSpeaker, replaceWords, lastSentence, lastSentenceInput
    try:


        #今の気持ちから考える
        if heart - 10 < 0:
            f = 0
        else:
            f = heart - 10

        if heart + 10 >= len(data["sentence"]) - 1:
            t = len(data["sentence"]) - 1
        else:
            t = heart + 50

        i = f
        ii = 0

        cc = []
        for sen in data["sentence"][f:t]:
            if i >= t:
                break
            into = x
            a = -1
            b = 1
            c = 0
            while True:
                if into in sen[0]:
                    c += 1
                try:
                    if len(x) == b:
                        cc[ii] = cc[ii] / ((len(x) + len(sen[0])) / 2)
                        c = c / ((len(x) + len(sen[0])) / 2)
                        
                        if len(cc) >= 2:
                            if cc[ii] - cc[ii-1] >= 0.75 or c >= 0.75:
                                print("A自信: {}".format(c))
                                print("A前との差: {}".format(cc[ii] - cc[ii-1]))
                                print("A類似発言: {}".format(data["sentence"][i][0]))
                                if reply:
                                    if settings["myname"] != data["sentence"][i+1][1] and not bool(re.search(settings["mynames"], data["sentence"][i+1][0])) and i != len(data["sentence"]) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+1][0]:
                                        heart = i+1
                                        heartLastSpeaker = data["sentence"][i+1][1]
                                        return data["sentence"][i+1][0]
                                else:
                                    heart = i
                                    return
                        break
                except:
                    break
                a += 1
                b += 1
                into = x[a:b]
                if len(cc) < ii+1:
                    while len(cc) < ii+1:
                        cc.append(c)
                cc[ii] = c
            i += 1
            ii += 1





        #今の気持ちから少し離れる
        if heart - 150 < 0:
            f = 0
        else:
            f = heart - 150

        if heart + 150 >= len(data["sentence"]) - 1:
            t = len(data["sentence"]) - 1
        else:
            t = heart + 150

        i = f
        ii = 0

        cc = []
        for sen in data["sentence"][f:t]:
            if i >= t:
                break
            into = x
            a = -1
            b = 1
            c = 0
            while True:
                if into in sen[0]:
                    c += 1
                try:
                    if len(x) == b:
                        cc[ii] = cc[ii] / ((len(x) + len(sen[0])) / 2)
                        c = c / ((len(x) + len(sen[0])) / 2)
                        
                        if len(cc) >= 2:
                            if cc[ii] - cc[ii-1] >= 0.75 or c >= 0.75:
                                print("B自信: {}".format(c))
                                print("B前との差: {}".format(cc[ii] - cc[ii-1]))
                                print("B類似発言: {}".format(data["sentence"][i][0]))
                                if reply:
                                    if settings["myname"] != data["sentence"][i+1][1] and not bool(re.search(settings["mynames"], data["sentence"][i+1][0])) and i != len(data["sentence"]) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+1][0]:
                                        heart = i+1
                                        heartLastSpeaker = data["sentence"][i+1][1]
                                        return data["sentence"][i+1][0]
                                else:
                                    heart = i
                                    return
                        break
                except:
                    break
                a += 1
                b += 1
                into = x[a:b]
                if len(cc) < ii+1:
                    while len(cc) < ii+1:
                        cc.append(c)
                cc[ii] = c
            i += 1
            ii += 1






        #より深く考える
        if heart - 300000 < 0:
            f = 0
        else:
            f = heart - 300000

        if heart + 300000 >= len(data["sentence"]) - 1:
            t = len(data["sentence"]) - 1
        else:
            t = heart + 300000

        i = f
        ii = 0

        cc = []
        for sen in data["sentence"][f:t]:
            if i >= t:
                break
            into = x
            a = -1
            b = 1
            c = 0
            while True:
                if into in sen[0]:
                    c += 1
                try:
                    if len(x) == b:
                        cc[ii] = cc[ii] / ((len(x) + len(sen[0])) / 2)
                        c = c / ((len(x) + len(sen[0])) / 2)
                        
                        if len(cc) >= 2:
                            if cc[ii] - cc[ii-1] >= 0.75 or c >= 0.75:
                                print("C自信: {}".format(c))
                                print("C前との差: {}".format(cc[ii] - cc[ii-1]))
                                print("C類似発言: {}".format(data["sentence"][i][0]))
                                if reply:
                                    if settings["myname"] != data["sentence"][i+1][1] and not bool(re.search(settings["mynames"], data["sentence"][i+1][0])) and i != len(data["sentence"]) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+1][0]:
                                        heart = i+1
                                        heartLastSpeaker = data["sentence"][i+1][1]
                                        return data["sentence"][i+1][0]
                                else:
                                    heart = i
                                    return
                        break
                except:
                    break
                a += 1
                b += 1
                into = x[a:b]
                if len(cc) < ii+1:
                    while len(cc) < ii+1:
                        cc.append(c)
                cc[ii] = c
            i += 1
            ii += 1



        #より深く考える
        if heart - 300000 < 0:
            f = 0
        else:
            f = heart - 300000

        if heart + 300000 >= len(data["sentence"]) - 1:
            t = len(data["sentence"]) - 1
        else:
            t = heart + 300000

        i = f
        ii = 0

        cc = []
        for sen in data["sentence"][f:t]:
            if i >= t:
                break
            into = x
            a = -1
            b = 1
            c = 0
            while True:
                if into in sen[0]:
                    c += 1
                try:
                    if len(x) == b:
                        cc[ii] = cc[ii] / ((len(x) + len(sen[0])) / 2)
                        c = c / ((len(x) + len(sen[0])) / 2)
                        
                        if len(cc) >= 2:
                            if cc[ii] - cc[ii-1] >= 0.5 or c >= 0.5:
                                print("D自信: {}".format(c))
                                print("D前との差: {}".format(cc[ii] - cc[ii-1]))
                                print("D類似発言: {}".format(data["sentence"][i][0]))
                                if reply:
                                    if settings["myname"] != data["sentence"][i+1][1] and not bool(re.search(settings["mynames"], data["sentence"][i+1][0])) and i != len(data["sentence"]) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+1][0]:
                                        heart = i+1
                                        heartLastSpeaker = data["sentence"][i+1][1]
                                        return data["sentence"][i+1][0]
                                else:
                                    heart = i
                                    return
                        break
                except:
                    break
                a += 1
                b += 1
                into = x[a:b]
                if len(cc) < ii+1:
                    while len(cc) < ii+1:
                        cc.append(c)
                cc[ii] = c
            i += 1
            ii += 1




        #より深く考える
        if heart - 300000 < 0:
            f = 0
        else:
            f = heart - 300000

        if heart + 300000 >= len(data["sentence"]) - 1:
            t = len(data["sentence"]) - 1
        else:
            t = heart + 300000

        i = f
        ii = 0

        cc = []
        for sen in data["sentence"][f:t]:
            if i >= t:
                break
            into = x
            a = -1
            b = 1
            c = 0
            while True:
                if into in sen[0]:
                    c += 1
                try:
                    if len(x) == b:
                        cc[ii] = cc[ii] / ((len(x) + len(sen[0])) / 2)
                        c = c / ((len(x) + len(sen[0])) / 2)
                        
                        if len(cc) >= 2:
                            if cc[ii] - cc[ii-1] >= 0.25 or c >= 0.25:
                                print("E自信: {}".format(c))
                                print("E前との差: {}".format(cc[ii] - cc[ii-1]))
                                print("E類似発言: {}".format(data["sentence"][i][0]))
                                if reply:
                                    if settings["myname"] != data["sentence"][i+1][1] and not bool(re.search(settings["mynames"], data["sentence"][i+1][0])) and i != len(data["sentence"]) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+1][0]:
                                        heart = i+1
                                        heartLastSpeaker = data["sentence"][i+1][1]
                                        return data["sentence"][i+1][0]
                                else:
                                    heart = i
                                    return
                        break
                except:
                    break
                a += 1
                b += 1
                into = x[a:b]
                if len(cc) < ii+1:
                    while len(cc) < ii+1:
                        cc.append(c)
                cc[ii] = c
            i += 1
            ii += 1





    except:
        import traceback
        traceback.print_exc()

    return None




def isNextAble():
    global heart
    if data["sentence"][heart+1][1] == heartLastSpeaker and heart+1 != len(data["sentence"]) and not bool(re.search(settings["mynames"], data["sentence"][heart+1][0])) and lastSentence != data["sentence"][heart+1][0] and lastSentenceInput != data["sentence"][heart+1][0]:
        return True
    else:
        return False

def tsuzuki(add=True):
    global heart, actualUser, brainUser, wordMemory, tokenizer, lastSentence
    
    heart += 1
    if heart >= len(data["sentence"]):
        heart = 0
    try:
        a = 0
        while True:
            if a >= 100:
                return None
            #if data["sentence"][heart][1] == heartLastSpeaker and heart != len(data["sentence"]) and not bool(re.search(settings["mynames"], data["sentence"][heart][0])) and lastSentence != data["sentence"][heart][0] and lastSentenceInput != data["sentence"][heart][0]:
            if data["sentence"][heart][1] == heartLastSpeaker and heart != len(data["sentence"]) and not bool(re.search(settings["mynames"], data["sentence"][heart][0])) and lastSentence != data["sentence"][heart][0] and lastSentenceInput != data["sentence"][heart][0]:
                result = data["sentence"][heart][0]
                lastSentence = result
                result = result.replace(data["sentence"][heart][1], settings["myname"])

                #重要な単語を最大5個置き換える
                try:
                    if replaceWords:
                        i = 0
                        while True:
                            if i == len(data["sentence"][heart][2]):
                                break
                            result = result.replace(data["sentence"][heart][2][i], wordMemory[i])
                            i += 1
                except:
                    import traceback
                    traceback.print_exc()


                i = 0
                while True:
                    if len(brainUser) >= i:
                        break
                    result = result.replace(brainUser[i], actualUser[i])
                    i += 1



                print("lastUser: {}".format(lastUser))


                if add: addSentence(result, settings["myname"])

                return result
            heart += 1
            if heart >= len(data["sentence"]):
                heart = 0
            a += 1
    except:
        import traceback
        traceback.print_exc()



def wordSyori(x):
    global tokenizer, wordMemory
    if len(wordMemory) >= 6:
        wordMemory = [wordMemory[-1], wordMemory[-2], wordMemory[-3], wordMemory[-4], wordMemory[-5]]

def addSentence(x, u, noword=False):
    #言葉を脳に記録する
    global data
    data["sentence"].append([x, u, wordMemory])
    if noword == False: wordSyori(x)


def save():
    global direc, data
    if len(data["sentence"]) >= 1000000:
        while len(data["sentence"]) >= 1000000:
            data["sentence"].pop()
    with open(direc+"/data.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    load()



def speakFreely(x, user, add=True):
    #自由に話す
    global heart, actualUser, brainUser, wordMemory, tokenizer, lastSentence, lastSentenceInput, maeheart, myVoice

    result = myVoice    
    if add and result != None: addSentence(result, settings["myname"])

    return result

def receive(x, u, add=True):
    global lastSentenceInput, myVoice
    if x == None or u == None: return
    lastSentenceInput = x
    lastUser = u
    if add: addSentence(x, u)
    result = looking(x)

    lastSentence = result
    if result == None:
        print("頭がパンクしそう...")
        myVoice = None
        return
    result = result.replace(data["sentence"][heart][1], settings["myname"])




    #重要な単語を最大5個置き換える
    try:
        if replaceWords:
            i = 0
            while True:
                if i == len(data["sentence"][heart][2]):
                    break
                result = result.replace(data["sentence"][heart][2][i], wordMemory[i])
                i += 1
    except:
        import traceback
        traceback.print_exc()


    i = 0
    while True:
        if len(brainUser) <= i:
            break
        result = result.replace(brainUser[i], actualUser[i])
        i += 1


    print("lastUser: {}".format(lastUser))


    print("現在の心: {}".format(heart))
    maeheart = heart
    
    myVoice = result
    print("心の声: {}".format(myVoice))


    if [u] not in data["users"]:
        data["users"].append([u])
    if [u] not in data["users"]:
        data["users"].append([settings["myname"]])

def addFact(x, y, z):
    data["fact"].append([x, y, [z]])


import atexit
def allDone():
    print("セーブします")
    save()
    print("完了")
atexit.register(allDone)

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
        elif into == "":
            exit()
        else:
            receive(into, "ゆいな")
            print("{}: {}".format(settings["myname"], speakFreely(into, "ゆいな")))
