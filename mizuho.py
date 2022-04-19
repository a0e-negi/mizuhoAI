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
import Levenshtein


data = None
settings = None
direc = None
actualUser = []
kazu = 0
wordMemory = ["None"]*5
heart = None
replaceWords = True
lastSentence = None
lastSentenceInput = None
heartLastSpeaker = None
getBored = 0
maeheart = 0
interface = 0

def initialize(direcectory, interface_):
    global data, settings, direc, heart, interface
    direc = direcectory
    interface = interface_
    with open(direc+"/data.json", "r", encoding="utf8") as f:
        data = json.load(f)
    with open(direc+"/settings.json", "r", encoding="utf8") as f:
        settings = json.load(f)
    heart = 0

def load():
    global data, direc
    with open(direc+"/data.json", "r", encoding="utf8") as f:
        data = json.load(f)


def looking(x, reply=True):
    global heart, heartLastSpeaker, replaceWords, lastSentence, lastSentenceInput
    try:
        into = x
        while True:
            if 0 == len(into): 
                break
            pattern = re.compile(r"{}$".format(into))
            i = heart
            for sen in data["sentence"][heart:-1]:
                if 4 > len(into):
                    replaceWords = False
                else:
                    replaceWords = True
                if bool(pattern.search(sen[0])) or (((len(x) + len(sen[0])) / 2) * 0.5) >= Levenshtein.distance(x, sen[0]):
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

        into = x
        while True:
            if 0 == len(into): 
                break
            pattern = re.compile(r"{}$".format(into))
            i = 0
            for sen in data["sentence"]:
                if bool(pattern.search(sen[0])) or (((len(x) + len(sen[0])) / 2) * 0.5) >= Levenshtein.distance(x, sen[0]):
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
                                if i+ii != len(data["sentence"]) and data["sentence"][i+ii+1][1] != settings["myname"] and not bool(re.search(settings["mynames"], data["sentence"][i+ii+1][0]))and lastSentence != data["sentence"][i+ii+1][0] and lastSentenceInput != data["sentence"][i+ii+1][0]:
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



    except:
        import traceback
        traceback.print_exc()
        
    return None

def isNextAble():
    if data["sentence"][heart+1][1] == heartLastSpeaker and heart+1 != len(data["sentence"]) and data["sentence"][heart+1][1] != settings["myname"] and not bool(re.search(settings["mynames"], data["sentence"][heart+1][0])) and lastSentence != data["sentence"][heart+1][0] and lastSentenceInput != data["sentence"][heart+1][0]:
        return True
    else:
        return False


def tsuzuki(add=True):
    global heart, actualUser, kazu, wordMemory, tokenizer, lastSentence
    
    heart += 1
    if heart >= len(data["sentence"]):
        heart = 0
    try:
        while True:
            if (data["sentence"][heart][1] == heartLastSpeaker or heartLastSpeaker == None) and heart != len(data["sentence"]) and data["sentence"][heart][1] != settings["myname"] and not bool(re.search(settings["mynames"], data["sentence"][heart][0])):
                result = data["sentence"][heart][0]
                lastSentence = result
                result = result.replace(data["sentence"][heart][1], settings["myname"])
                
                brainUser = []
                i = 0
                ii = 0
                for u in data["users"]:
                    if u[0] == data["sentence"][heart][1]:
                        brainUser.append(u[0])
                        ii += 1
                    if ii >= kazu:
                        break
                    i += 1
                kazu = ii
                brainUser.append(data["sentence"][heart][1])
                
                
                i = 1
                if kazu > 0:
                    i = 0
                    while True:
                        if i >= kazu:
                            break
                        result = result.replace(brainUser[i], actualUser[i])
                        i += 1


                try:
                    if replaceWords:
                        i = 0
                        while True:
                            if len(wordMemory) == len(data["sentence"][heart][2]):
                                if i == len(data["sentence"][heart][2]):
                                    break
                                result = result.replace(data["sentence"][heart][2][i], wordMemory[i])
                                i += 1
                            if len(wordMemory) < len(data["sentence"][heart][2]):
                                if i == len(wordMemory):
                                    break
                                result = result.replace(data["sentence"][heart][2][i], wordMemory[i])
                                i += 1
                            if len(wordMemory) > len(data["sentence"][heart][2]):
                                if i == len(data["sentence"][heart][2]):
                                    break
                                result = result.replace(data["sentence"][heart][2][i], wordMemory[i])
                                i += 1
                except:
                    import traceback
                    traceback.print_exc()

                if add: addSentence(result, settings["myname"])


                return result
            heart += 1
            if heart >= len(data["sentence"]):
                heart = 0
    except:
        import traceback
        traceback.print_exc()

def wordSyori(x):
    global tokenizer, wordMemory
    if len(wordMemory) >= 6:
        wordMemory = [wordMemory[-1], wordMemory[-2], wordMemory[-3], wordMemory[-4], wordMemory[-5]]

def addSentence(x, u, noword=False):
    global data
    data["sentence"].append([x, u, wordMemory])
    save()
    if noword == False: wordSyori(x)


def save():
    global direc, data
    if len(data["sentence"]) >= 100000000:
        while len(data["sentence"]) >= 100000000:
            data["sentence"].pop()
    with open(direc+"/data.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    load()



def speakFreely(x, user, add=True):
    global heart, actualUser, kazu, wordMemory, tokenizer, lastSentence, lastSentenceInput, getBored, maeheart

    if -20 <= heart - maeheart and heart - maeheart <= 20:
        getBored += 1
        print("飽きかけてる: {}".format(heart - maeheart))
    elif getBored > 0:
        getBored -= 2
    elif getBored - 2 < 0:
        getBored = 0
    print("飽き度: {}".format(getBored))

    if getBored >= 15:
        getBored = 0
        heart = 0
        print("飽きたので別の話")

    result = looking(x)
    lastSentence = result
    if result == None:
        return None
    result = result.replace(data["sentence"][heart][1], settings["myname"])
    
    AU = []
    i = 0
    ii = 0
    for u in data["users"]:
        if u[0] == user:
            AU.append(u[0])
            ii += 1
        if len(AU) >= 3:
            break
        i += 1
    kazu = ii
    if AU != []:
        actualUser = AU
        actualUser.append(user)
    print("actualUser: {}".format(actualUser))


    brainUser = []
    i = 0
    ii = 0
    for u in data["users"]:
        if u[0] == data["sentence"][heart][1]:
            brainUser.append(u[0])
            ii += 1
        if ii >= kazu:
            break
        i += 1
    kazu = ii
    brainUser.append(data["sentence"][heart][1])
    brainUser = brainUser[kazu-1:-1]

    try:
        if replaceWords:
            i = 0
            while True:
                if len(wordMemory) == len(data["sentence"][heart][2]):
                    if i == len(data["sentence"][heart][2]):
                        break
                    result = result.replace(data["sentence"][heart][2][i], wordMemory[i])
                    i += 1
                if len(wordMemory) < len(data["sentence"][heart][2]):
                    if i == len(wordMemory):
                        break
                    result = result.replace(data["sentence"][heart][2][i], wordMemory[i])
                    i += 1
                if len(wordMemory) > len(data["sentence"][heart][2]):
                    if i == len(data["sentence"][heart][2]):
                        break
                    result = result.replace(data["sentence"][heart][2][i], wordMemory[i])
                    i += 1
    except:
        import traceback
        traceback.print_exc()


    if kazu > 0:
        i = 0
        while True:
            if i >= kazu:
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
            print("みずほ: {}".format(speakFreely(into, "ゆいな")))