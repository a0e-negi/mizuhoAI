
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
getBored = 0
interface = 0 #クライアントの種類
lastUser = "あなた" #最後に話しかけたユーザー
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
    heart = len(data["sentence"]) - 1
    with open(direc+"/data_backup.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def looking(x, reply=True):
    #過去の発言をもとに考える
    global heart, heartLastSpeaker, replaceWords, lastSentence, lastSentenceInput
    try:

        for i in range(5):
            if i == 0:
                rate = 1
            if i == 1:
                rate = 0.8
            if i == 2:
                rate = 0.6
            if i == 3:
                rate = 0.4
            if i == 4:
                rate = 0.2

            #今の気持ちから考える
            if heart < 0:
                f = 0
            else:
                f = heart

            if heart + 50 >= len(data["sentence"]) - 1:
                t = len(data["sentence"]) - 1
            else:
                t = heart + 50

            i = f
            ii = 0
            kon = -1
            zen = -1

            cc = [0]
            for sen in data["sentence"][f:t]:
                into = x
                a = -1
                b = 1
                c = 0
                while True:
                    zen = kon
                    kon = i
                    if into in sen[0]:
                        c += 1
                    if len(x) == b:
                        cc[-1] = cc[-1] / ((len(x) + len(sen[0])) / 2)
                        c = c / ((len(x) + len(sen[0])) / 2)
                        
                        if len(cc) >= 2:
                            if cc[-1] - cc[-2] >= rate or c >= rate:
                                print("類似: {}".format(data["sentence"][i][0]))
                                for iii in range(3):
                                    if i+1+iii >= len(data["sentence"]) - 1:
                                        break
                                    if reply:
                                        if settings["myname"] != data["sentence"][i+1+iii][1] and i != len(data["sentence"]) and lastSentence != data["sentence"][i+1+iii][0] and lastSentenceInput != data["sentence"][i+1+iii][0]:
                                            flag = True
                                            for iiiii in range(15):
                                                if i+1+iii+iiiii < len(data["sentence"]) - 1:
                                                    if data["sentence"][i+1+iii+iiiii][0] == "×":
                                                        flag = False
                                                        break
                                            if data["sentence"][i+1][0] == "×":
                                                heart = i+1
                                                heartLastSpeaker = data["sentence"][i+1][1]
                                                return "×"
                                            if flag:
                                                heart = i+1+iii
                                                heartLastSpeaker = data["sentence"][i+1+iii][1]
                                                return data["sentence"][i+1+iii][0]
                                    else:
                                        heart = i
                                        return
                        break
                    a += 1
                    b += 1
                    into = x[a:b]
                    if kon != zen:
                        cc.append(c)
                    cc[-1] = c
                    if len(cc) >= 2:
                        cc = cc[-2:]
                        cc[1] = c
                    else:
                        cc[-1] = c
                i += 1
                ii += 1




            #今の気持ちから少し離れる
            if heart - 1500 < 0:
                f = 0
            else:
                f = heart - 1500

            if heart + 1500 >= len(data["sentence"]) - 1:
                t = len(data["sentence"]) - 1
            else:
                t = heart + 1500

            i = f
            ii = 0
            kon = -1
            zen = -1

            cc = [0]
            for sen in data["sentence"][f:t]:
                into = x
                a = -1
                b = 1
                c = 0
                while True:
                    zen = kon
                    kon = i
                    if into in sen[0]:
                        c += 1
                    if len(x) == b:
                        cc[-1] = cc[-1] / ((len(x) + len(sen[0])) / 2)
                        c = c / ((len(x) + len(sen[0])) / 2)
                        
                        if len(cc) >= 2:
                            if cc[-1] - cc[-2] >= rate or c >= rate:
                                print("類似: {}".format(data["sentence"][i][0]))
                                for iii in range(3):
                                    if i+1+iii >= len(data["sentence"]) - 1:
                                        break
                                    if reply:
                                        if settings["myname"] != data["sentence"][i+1+iii][1] and i != len(data["sentence"]) and lastSentence != data["sentence"][i+1+iii][0] and lastSentenceInput != data["sentence"][i+1+iii][0]:
                                            flag = True
                                            for iiiii in range(15):
                                                if i+1+iii+iiiii < len(data["sentence"]) - 1:
                                                    if data["sentence"][i+1+iii+iiiii][0] == "×":
                                                        flag = False
                                                        break
                                            if flag:
                                                heart = i+1+iii
                                                heartLastSpeaker = data["sentence"][i+1+iii][1]
                                                return data["sentence"][i+1+iii][0]
                                    else:
                                        heart = i
                                        return
                        break
                    a += 1
                    b += 1
                    into = x[a:b]
                    if kon != zen:
                        cc.append(c)
                    cc[-1] = c
                    if len(cc) >= 2:
                        cc = cc[-2:]
                        cc[1] = c
                    else:
                        cc[-1] = c
                i += 1
                ii += 1





            #より深く考える
            if heart - 60000 < 0:
                f = 0
            else:
                f = heart - 60000

            if heart + 60000 >= len(data["sentence"]) - 1:
                t = len(data["sentence"]) - 1
            else:
                t = heart + 60000

            i = f
            ii = 0
            kon = -1
            zen = -1

            cc = [0]
            for sen in data["sentence"][f:t]:
                into = x
                a = -1
                b = 1
                c = 0
                while True:
                    zen = kon
                    kon = i
                    if into in sen[0]:
                        c += 1
                    if len(x) == b:
                        cc[-1] = cc[-1] / ((len(x) + len(sen[0])) / 2)
                        c = c / ((len(x) + len(sen[0])) / 2)
                        
                        if len(cc) >= 2:
                            if cc[-1] - cc[-2] >= rate or c >= rate:
                                print("類似: {}".format(data["sentence"][i][0]))
                                for iii in range(3):
                                    if i+1+iii >= len(data["sentence"]) - 1:
                                        break
                                    if reply:
                                        if settings["myname"] != data["sentence"][i+1+iii][1] and i != len(data["sentence"]) and lastSentence != data["sentence"][i+1+iii][0] and lastSentenceInput != data["sentence"][i+1+iii][0]:
                                            flag = True
                                            for iiiii in range(15):
                                                if i+1+iii+iiiii < len(data["sentence"]) - 1:
                                                    if data["sentence"][i+1+iii+iiiii][0] == "×":
                                                        flag = False
                                                        break
                                            if flag:
                                                heart = i+1+iii
                                                heartLastSpeaker = data["sentence"][i+1+iii][1]
                                                return data["sentence"][i+1+iii][0]
                                        else:
                                            continue
                                    else:
                                        heart = i
                                        return
                        break
                    a += 1
                    b += 1
                    into = x[a:b]
                    if kon != zen:
                        cc.append(c)
                    cc[-1] = c
                    if len(cc) >= 2:
                        cc = cc[-2:]
                        cc[1] = c
                    else:
                        cc[-1] = c
                i += 1
                ii += 1







    except:
        import traceback
        traceback.print_exc()

    return tsuzuki()




def tsuzuki(add=True):
    global heart, actualUser, brainUser, wordMemory, tokenizer, lastSentence
    
    heart += 1
    if heart >= len(data["sentence"]):
        heart = 0
    try:
        a = 0
        while True:
            if a >= 60000:
                return None
            if heart != len(data["sentence"]) - 1 and lastSentence != data["sentence"][heart][0] and lastSentenceInput != data["sentence"][heart][0]:

                flag = True
                for iiiii in range(15):
                    if heart+iiiii < len(data["sentence"]) - 1:
                        if data["sentence"][heart+iiiii][0] == "×":
                            flag = False
                if flag:

                    result = data["sentence"][heart][0]
                    lastSentence = result

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




                    #名前置き換え用
                    brainUser.append(data["sentence"][heart-1][1])
                    if len(brainUser) > 5:
                        brainUser = [brainUser[-5], brainUser[-4], brainUser[-3], brainUser[-2], brainUser[-1]]
                    
                    actualUser.append(lastUser)
                    if len(actualUser) > 5:
                        actualUser = [actualUser[-5], actualUser[-4], actualUser[-3], actualUser[-2], actualUser[-1]]

                    for i in range(len(actualUser)):
                        result = result.replace(brainUser[i], actualUser[i])




                    if add: addSentence(result, settings["myname"])

                    return result
            heart += 1
            if heart >= len(data["sentence"]):
                heart = len(data["sentence"]) - 100
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
    if len(data["sentence"]) >= 10000000:
        while len(data["sentence"]) >= 10000000:
            del data["sentence"][0]
    with open(direc+"/data.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))



def speakFreely(add=True):
    #自由に話す
    global heart, actualUser, brainUser, wordMemory, tokenizer, lastSentence, lastSentenceInput, maeheart, myVoice

    if lastSentenceInput != "×":
        result = myVoice    
        if add and result != None: addSentence(result, settings["myname"])

        print("brainUser: {}".format(brainUser))
        print("actualUser: {}".format(actualUser))

        return result

def receive(x, u, add=True):
    global lastSentenceInput, lastSentence, myVoice, getBored, maeheart, heart, actualUser, brainUser
    try:
        if x == None or u == None: return
        lastSentenceInput = x
        lastUser = u
        if add: addSentence(x, u)

        result = looking(x)

        if result == None:
            getBored += 1
            myVoice = None
            return



        #名前置き換え用
        brainUser.append(data["sentence"][heart-1][1])
        if len(brainUser) > 5:
            brainUser = [brainUser[-5], brainUser[-4], brainUser[-3], brainUser[-2], brainUser[-1]]
        
        actualUser.append(u)
        if len(actualUser) > 5:
            actualUser = [actualUser[-5], actualUser[-4], actualUser[-3], actualUser[-2], actualUser[-1]]

        for i in range(len(actualUser)):
            result = result.replace(brainUser[i], actualUser[i])



        if x == "×" and (heart < len(data["sentence"]) - 10 or heart > len(data["sentence"]) + 10):
            data["sentence"].insert(heart+1, ["×", settings["myname"], wordMemory])

        if data["sentence"][heart+1][0] == "×":
            myVoice = "×"
            return

        lastSentence = result




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
            return None


        
        myVoice = result


        if [u] not in data["users"]:
            data["users"].append([u])
        if [u] not in data["users"]:
            data["users"].append([settings["myname"]])


        #既存の文化に飽きさせる2
        if -16 <= heart - maeheart and heart - maeheart <= 16:
            getBored += 1
        else:
            getBored -= 0.5
        if getBored < 0:
            getBored = 0

        if getBored >= 4:
            getBored = 0
            heart_ = heart
            heart = random.randint(0, len(data["sentence"]) - 50)
            if 0 > heart_-1: looking(data["sentence"][heart_-1][0])
            looking(data["sentence"][heart_][0])

        maeheart = heart
    except:
        import traceback
        traceback.print_exc()
        return None



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
            print("{}: {}".format(settings["myname"], speakFreely()))
