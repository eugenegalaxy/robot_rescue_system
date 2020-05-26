#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from gtts import gTTS 
import os 
import speech_recognition as sr
import time
from InternetTest import *
from googletrans import Translator
from OfflineVoice import *
import random
from collections import Counter
import logging

def recognize_speech_from_mic(recognizer, microphone, lang):

    
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language=lang) #show_all=True = gives all possibilities
 


    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
        if response["error"] == "API unavailable":
            print("Going Offline")
            time.sleep(2)
            Offline = True
            while Offline == True: 
                OfflineVoice()
                print("")
            

    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response


def Test_speech(lang, name):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    translator = Translator()
    translated = translator.translate('Hello', dest=lang)
    mytext = translated.text + ' ' + name 
    language = lang
    myobj = gTTS(text=mytext, lang=language, slow=False) 
    myobj.save("welcome.mp3") 
    os.system("mpg321 -q welcome.mp3")    
    if lang == 'sv':
        randomword = [ "rebecka","hem","skola","kontor", "onsdag", "fredag", "lördag", "jordbävning","ja", "nej", "huvud", "hand", "mage", "buk", "bröst"]
    elif lang == 'da': 
        randomword = [ "dariush","hjem","skole","kontor", "onsdag", "fredag", "lørdag", "jordskælv","ja", "nej", "hoved", "hånd", "mave", "underliv", "brøst"]
    elif lang == 'ru':
        randomword = [ "евгений","дом","школа","офис", "среда", "пятница", "суббота", "землетрясение","да", "нет", "голова", "рука", "желудок", "живот", "грудь"] #"евгений" = Jevgenijs
    else:
        randomword = [ "rebecca","home","school","office", "wednesday", "friday", "saturday", "earthquake","yes", "no", "head", "hand", "stomach", "abdomen", "chest"]
    counter = 0
    i = 0
    sucsesses = []
    failures = []
    no_detection = []
    while(1): 
        while (1):
            while (1):
                counter += 1
                if counter == 101:
                    translator = Translator()
                    translated = translator.translate('Tack för idag, det var allt jag har at bjuda på', dest=lang)
                    mytext = translated.text  
                    language = lang
                    myobj = gTTS(text=mytext, lang=language, slow=False) 
                    myobj.save("welcome.mp3") 
                    os.system("mpg321 -q welcome.mp3")  
                    SucsessfullDetection=Counter(sucsesses)
                    FailedDetection=Counter(failures)
                    NoDetection=Counter(no_detection)
                    print("Sucsess ", SucsessfullDetection)
                    print("Failure ", FailedDetection)
                    print("No detection ", NoDetection)
                    path = os.path.dirname(os.path.abspath(__file__))
                    local_path = "tests/test_log.log"
                    full_path = os.path.join(path, local_path)
                    logging.basicConfig(filename = full_path,level=logging.DEBUG,format='%(asctime)s :: %(message)s')
                    logging.info('Number of attempts:')
                    logging.info(counter)
                    logging.info('Sucsess:')
                    logging.info(SucsessfullDetection)
                    logging.info('Failure:')
                    logging.info(FailedDetection)
                    logging.info('No detection:')
                    logging.info(NoDetection)
                    exit()
                print (counter)
                theRandomWord = (random.choice(randomword))
                translator = Translator()
                translated = translator.translate('Vänligen säg en fras med ordet ,  ,   ', dest=lang)
                mytext = translated.text + theRandomWord
                myobj = gTTS(text=mytext, lang=language, slow=False) 
                myobj.save("welcome.mp3") 
                os.system("mpg321 -q welcome.mp3")    
                print(theRandomWord)

                if lang == 'da':
                    guess = recognize_speech_from_mic(recognizer, microphone, 'da-DK')
                elif lang == 'sv':
                    guess = recognize_speech_from_mic(recognizer, microphone, 'sv-SE')
                elif lang == 'ru':
                    guess = recognize_speech_from_mic(recognizer, microphone, 'ru-RU')
                else :
                    guess = recognize_speech_from_mic(recognizer, microphone, 'en-UK')
                if guess["transcription"]:
                    break
                if not guess["success"]:
                    break
                no_detection.extend([theRandomWord])
                
                
                print("I didn't catch that. What did you say?\n")

            if guess["error"]:
                print("ERROR: {}".format(guess["error"]))
                break
            #print("You said: {}".format(guess["transcription"]))
        
            message = guess["transcription"].lower()                
            if theRandomWord in message: 
                sucsesses.extend([theRandomWord])
                #print('Successfully Detected The Words', sucsesses)
            else:
                #print('Wrongly Detected The Word', theRandomWord)
                failures.extend([theRandomWord])


def count_number(word, sentence):
    return sentence.lower().split().count(word)
    
if __name__ == "__main__":

    Test_speech('da', 'dariush')

