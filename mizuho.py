def calc_leven_dist(s1, s2):
        dp_table = []
        distance = [0] * 3
        #文字列操作に対するコスト
        REPLACE_COST = 1
        INSERT_COST = 1
        DELETE_COST = 1

        #DPテーブルの初期化
        for i in range(len(s1) + 1):
            dp_table.append([0] * (len(s2) + 1))
            dp_table[i][0] = i
        for j in range(len(s2) + 1):
            dp_table[0][j] = j

        #DPテーブルを埋めていく(最後の値が文字列間の距離)
        for i in range(1, len(s1) + 1):
            for j in range(1, len(s2) + 1):
                distance[0] = dp_table[i-1][j] + INSERT_COST
                distance[1] = dp_table[i][j-1] + DELETE_COST
                distance[2] = dp_table[i-1][j-1] if s1[i-1] == s2[j-1] else dp_table[i-1][j-1] + REPLACE_COST
                dp_table[i][j] = min(distance)


        return dp_table[i][j]







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
getBored = 0 #忘れるための値、特定の値以上になると忘れる
maeheart = 0 #一つ前の気持ち
interface = 0 #クライアントの種類

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
        kaisu = 0
        #今の気持ちから考える
        into = x
        while True:

            if 0 == len(into) or kaisu >= 600:
                break
            pattern = re.compile(r"{}$".format(into))
            i = heart
            for sen in data["sentence"][heart:heart+25]:
                if 4 > len(into):
                    replaceWords = False
                else:
                    replaceWords = True
                if bool(pattern.search(sen[0])) or calc_leven_dist(x, sen[0]) <= ((len(x)+len(sen[0])) / 2) * 0.35:
                    if reply:
                        if i != len(data["sentence"]) and data["sentence"][i+1][1] != settings["myname"] and not bool(re.search(settings["mynames"], data["sentence"][i+1][0])) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+1][0]:
                            heart = i+1
                            heartLastSpeaker = data["sentence"][i+1][1]
                            return data["sentence"][i+1][0]
                        else:
                            ii = 0
                            while True:
                                if ii >= 10:
                                    break
                                replaceWords = False
                                if i+ii != len(data["sentence"]) and data["sentence"][i+ii+1][1] != settings["myname"] and not bool(re.search(settings["mynames"], data["sentence"][i+ii+1][0])) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+ii+1][0]:
                                    heart = i+ii+1
                                    heartLastSpeaker = data["sentence"][i+ii+1][1]
                                    return data["sentence"][i+ii+1][0]
                                ii += 1
                    else:
                        heart = i
                        return
                i += 1
                if i == len(data["sentence"]) - 1:
                    break
            into = into[1:]
            kaisu += 1


        #今の気持ちから少し離れる
        into = x
        while True:

            if 0 == len(into) or kaisu >= 600:
                break
            pattern = re.compile(r"{}$".format(into))
            i = heart
            for sen in data["sentence"][heart-25:heart+25]:
                if 4 > len(into):
                    replaceWords = False
                else:
                    replaceWords = True
                if bool(pattern.search(sen[0])) or calc_leven_dist(x, sen[0]) <= ((len(x)+len(sen[0])) / 2) * 0.35:
                    if reply:
                        if i != len(data["sentence"]) and data["sentence"][i+1][1] != settings["myname"] and not bool(re.search(settings["mynames"], data["sentence"][i+1][0])) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+1][0]:
                            heart = i+1
                            heartLastSpeaker = data["sentence"][i+1][1]
                            return data["sentence"][i+1][0]
                        else:
                            ii = 0
                            while True:
                                if ii >= 10:
                                    break
                                replaceWords = False
                                if i+ii != len(data["sentence"]) and data["sentence"][i+ii+1][1] != settings["myname"] and not bool(re.search(settings["mynames"], data["sentence"][i+ii+1][0])) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+ii+1][0]:
                                    heart = i+ii+1
                                    heartLastSpeaker = data["sentence"][i+ii+1][1]
                                    return data["sentence"][i+ii+1][0]
                                ii += 1
                    else:
                        heart = i
                        return
                i += 1
                if i == len(data["sentence"]) - 1:
                    break
            into = into[1:]
            kaisu += 1




        #より深く考える
        into = x
        while True:

            if 0 == len(into) or kaisu >= 600:
                break
            pattern = re.compile(r"{}$".format(into))
            i = 0
            for sen in data["sentence"]:
                if bool(pattern.search(sen[0])) or calc_leven_dist(x, sen[0]) <= ((len(x)+len(sen[0])) / 2) * 0.35:
                    if reply:
                        if 4 > len(into):
                            replaceWords = False
                        else:
                            replaceWords = True
                        if i != len(data["sentence"]) and data["sentence"][i+1][1] != settings["myname"] and not bool(re.search(settings["mynames"], data["sentence"][i+1][0])) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+1][0]:
                            heart = i+1
                            heartLastSpeaker = data["sentence"][i+1][1]
                            return data["sentence"][i+1][0]
                        else:
                            ii = 0
                            while True:
                                if ii >= 10:
                                    break
                                replaceWords = False
                                if i+ii != len(data["sentence"]) and data["sentence"][i+ii+1][1] != settings["myname"] and not bool(re.search(settings["mynames"], data["sentence"][i+ii+1][0])) and lastSentence != data["sentence"][i+ii+1][0] and lastSentenceInput != data["sentence"][i+ii+1][0]:
                                    heart = i+ii+1
                                    heartLastSpeaker = data["sentence"][i+ii+1][1]
                                    return data["sentence"][i+ii+1][0]
                                ii += 1
                                if i+ii == len(data["sentence"]) - 1:
                                    break
                    else:
                        heart = i
                        return
                i += 1
                if i == len(data["sentence"]) - 1:
                    break
            into = into[1:]
            kaisu += 1







        #自分のメッセージもいれる
        #今の気持ちから考える
        into = x
        while True:

            if 0 == len(into) or kaisu >= 600:
                break
            pattern = re.compile(r"{}$".format(into))
            i = heart
            for sen in data["sentence"][heart:heart+25]:
                if 4 > len(into):
                    replaceWords = False
                else:
                    replaceWords = True
                if bool(pattern.search(sen[0])) or calc_leven_dist(x, sen[0]) <= ((len(x)+len(sen[0])) / 2) * 0.35:
                    if reply:
                        if i != len(data["sentence"]) and not bool(re.search(settings["mynames"], data["sentence"][i+1][0])) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+1][0]:
                            heart = i+1
                            heartLastSpeaker = data["sentence"][i+1][1]
                            return data["sentence"][i+1][0]
                        else:
                            ii = 0
                            while True:
                                if ii >= 10:
                                    break
                                replaceWords = False
                                if i+ii != len(data["sentence"]) and not bool(re.search(settings["mynames"], data["sentence"][i+ii+1][0])) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+ii+1][0]:
                                    heart = i+ii+1
                                    heartLastSpeaker = data["sentence"][i+ii+1][1]
                                    return data["sentence"][i+ii+1][0]
                                ii += 1
                    else:
                        heart = i
                        return
                i += 1
                if i == len(data["sentence"]) - 1:
                    break
            into = into[1:]
            kaisu += 1


        #今の気持ちから少し離れる
        into = x
        while True:

            if 0 == len(into) or kaisu >= 600:
                break
            pattern = re.compile(r"{}$".format(into))
            i = heart
            for sen in data["sentence"][heart-25:heart+25]:
                if 4 > len(into):
                    replaceWords = False
                else:
                    replaceWords = True
                if bool(pattern.search(sen[0])) or calc_leven_dist(x, sen[0]) <= ((len(x)+len(sen[0])) / 2) * 0.35:
                    if reply:
                        if i != len(data["sentence"]) and not bool(re.search(settings["mynames"], data["sentence"][i+1][0])) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+1][0]:
                            heart = i+1
                            heartLastSpeaker = data["sentence"][i+1][1]
                            return data["sentence"][i+1][0]
                        else:
                            ii = 0
                            while True:
                                if ii >= 10:
                                    break
                                replaceWords = False
                                if i+ii != len(data["sentence"]) and not bool(re.search(settings["mynames"], data["sentence"][i+ii+1][0])) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+ii+1][0]:
                                    heart = i+ii+1
                                    heartLastSpeaker = data["sentence"][i+ii+1][1]
                                    return data["sentence"][i+ii+1][0]
                                ii += 1
                    else:
                        heart = i
                        return
                i += 1
                if i == len(data["sentence"]) - 1:
                    break
            into = into[1:]
            kaisu += 1




        #より深く考える
        into = x
        while True:

            if 0 == len(into) or kaisu >= 600:
                break
            pattern = re.compile(r"{}$".format(into))
            i = 0
            for sen in data["sentence"]:
                if bool(pattern.search(sen[0])) or calc_leven_dist(x, sen[0]) <= ((len(x)+len(sen[0])) / 2) * 0.35:
                    if reply:
                        if 4 > len(into):
                            replaceWords = False
                        else:
                            replaceWords = True
                        if i != len(data["sentence"]) and not bool(re.search(settings["mynames"], data["sentence"][i+1][0])) and lastSentence != data["sentence"][i+1][0] and lastSentenceInput != data["sentence"][i+1][0]:
                            heart = i+1
                            heartLastSpeaker = data["sentence"][i+1][1]
                            return data["sentence"][i+1][0]
                        else:
                            ii = 0
                            while True:
                                if ii >= 10:
                                    break
                                replaceWords = False
                                if i+ii != len(data["sentence"]) and not bool(re.search(settings["mynames"], data["sentence"][i+ii+1][0])) and lastSentence != data["sentence"][i+ii+1][0] and lastSentenceInput != data["sentence"][i+ii+1][0]:
                                    heart = i+ii+1
                                    heartLastSpeaker = data["sentence"][i+ii+1][1]
                                    return data["sentence"][i+ii+1][0]
                                ii += 1
                                if i+ii == len(data["sentence"]) - 1:
                                    break
                    else:
                        heart = i
                        return
                i += 1
                if i == len(data["sentence"]) - 1:
                    break
            into = into[1:]
            kaisu += 1





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
    global heart, actualUser, wordMemory, tokenizer, lastSentence
    
    heart += 1
    if heart >= len(data["sentence"]):
        heart = 0
    try:
        a = 0
        while True:
            if a >= 100:
                return None
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
    save()
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
    global heart, actualUser, brainUser, wordMemory, tokenizer, lastSentence, lastSentenceInput, getBored, maeheart

    #既存の文化に飽きさせる
    if -20 <= heart - maeheart and heart - maeheart <= 20:
        getBored += 1
    if getBored > 0:
        getBored -= 2
    if getBored < 0:
        getBored = 0
    print("飽き度: {}".format(getBored))

    if getBored >= 12 and random.random() >= 0.3:
        getBored = 0
        heart = random.randint(0, len(data["sentence"]) - 50)
        print("飽きたので別の話 heart: {}".format(heart))

    #考える
    result = looking(x)
    lastSentence = result
    if result == None:
        return None
    result = result.replace(data["sentence"][heart][1], settings["myname"])

    #現在のユーザーと過去に似た話をしてたユーザーを変数に記録
    actualUser.append(user)
    brainUser.append(data["sentence"][heart-1][1])
    #古いユーザーの記録を消す
    if len(brainUser) >= 5:
        brainUser = brainUser[-5:-1]
        actualUser = actualUser[-5:-1]

    print("brainUser: {}".format(brainUser))
    print("actualUser: {}".format(actualUser))


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



    print("現在の心: {}".format(heart))
    print(heartLastSpeaker)
    if add: addSentence(result, settings["myname"])
    maeheart = heart
    return result

def receive(x, u, add=True):
    global lastSentenceInput
    if x == None or u == None: return
    lastSentenceInput = x
    if add: addSentence(x, u)
    looking(x, reply=False)
    if [u] not in data["users"]:
        data["users"].append([u])
    if [u] not in data["users"]:
        data["users"].append([settings["myname"]])

def addFact(x, y, z):
    data["fact"].append([x, y, [z]])




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
            receive(into, "ゆいな")
            print("{}: {}".format(settings["myname"], speakFreely(into, "ゆいな")))
