import mizuho
import sys

if sys.argv[1]:
    mizuho.initialize(sys.argv[1], "assistant")
else:
    print("人格フォルダを指定してください。")
    exit()


import os
import subprocess
import time
import re
import requests



from pydub import AudioSegment
from pydub.playback import play

sound2 = AudioSegment.from_file("./se/2.wav", format="wav")
sound1 = AudioSegment.from_file("./se/1.wav", format="wav")

from gtts import gTTS




def speak(result):
    global channel, persons, boyomi
    pattern = re.compile(r"^!command")
    if bool(pattern.search(result)):
        com = result.split(" ")
        if com[1] == "discMove":
            pass
        elif com[1] == "ignore":
            pass
        elif com[1] == "modeChange":
            pass
    else:
        if mizuho.settings["language"] == "ja-vv":
            urlData = requests.get("https://tts-api.f5.si/v1/?speaker={}&pitch=0&intonationScale=1&speed=1&text={}".format(mizuho.settings["voice"], result)).content
            with open("./output/out.wav" ,mode='wb') as f: # wb でバイト型を書き込める
                f.write(urlData)
        else:
            tts = gTTS("{}".format(result), lang=mizuho.settings["language"])
            tts.save("./output/out.wav")

        play(sound1)
        print("{}: {}".format(mizuho.settings["myname"], result))
        sound = AudioSegment.from_mp3("./output/out.wav")
        play(sound)


import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()


while True:
    
    print("聞き取っています...")
    play(sound2)

    with mic as source:
        r.adjust_for_ambient_noise(source) #雑音対策
        audio = r.listen(source)

    print ("解析中...")

    try:
        into = r.recognize_google(audio, language=mizuho.settings["languageHear"])
        print(into)
        
        mizuho.receive(into, "あなた")
        result = mizuho.speakFreely()
        if result != None:
            speak(result)

    # 以下は認識できなかったときに止まらないように。
    except sr.UnknownValueError:
        print("沈黙を検知")
        mizuho.receive("!command ignore", "_BRAIN_")
        result = mizuho.speakFreely()
        if result != None:
            speak(result)
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
