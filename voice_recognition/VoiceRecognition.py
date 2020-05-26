#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from gtts import gTTS 
import os 
import speech_recognition as sr
import time
from InternetTest import *
#from keyboardControll import *
from googletrans import Translator
from OfflineVoice import *


def recognize_speech_from_mic(recognizer, microphone, lang):

    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, language=lang)
        # language='se-SE'
        # language='ru-RU'
        # language='en-UK')

    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
        if response["error"] == "API unavailable":
            print("Oh Shit")
            time.sleep(0.1)
            Offline = True
            if Offline == True: 
                response["transcription"] = OfflineVoice()
                #print("Something funny")
                

    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def motion_speech(lang, name):
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    translator = Translator()
    translated = translator.translate('Hello', dest=lang)
    mytext = translated.text + ' ' + name 
    language = lang
    myobj = gTTS(text=mytext, lang=language, slow=False) 
    myobj.save("welcome.mp3") 
    os.system("mpg321 -q welcome.mp3")    
    while(1): 
        while (1):
            while (1):	
                Connection = CheckingConnectionToGoogle()
                if Connection[0] == True: 
                    print(Connection, "Connected")

                elif Connection == False:
                    print("Connection lost")
                print("Recording Message")
                if lang == 'da':
                    guess = recognize_speech_from_mic(recognizer, microphone, 'da-DK')
                elif lang == 'sv':
                    guess = recognize_speech_from_mic(recognizer, microphone, 'sv-SE')
                elif lang == 'ru':
                    guess = recognize_speech_from_mic(recognizer, microphone, 'ru_RU')
                else :
                    guess = recognize_speech_from_mic(recognizer, microphone, 'en-UK')
                if guess["transcription"]:
                    break
                if not guess["success"]:
                    break
                print("I didn't catch that. What did you say?\n")

            # if there was an error, stop
            if guess["error"]:
                print("ERROR: {}".format(guess["error"]))
                break

            # show the user the transcription
            print("You said: {}".format(guess["transcription"]))
            message = guess["transcription"].lower() 
            #### Fun #####
            mytext = "You said" + "      " + message
            myobj = gTTS(text=mytext, lang=language, slow=False) 
            myobj.save("welcome.mp3") 
            os.system("mpg321 -q welcome.mp3")  
            ### No More Fun ###
            translated_stop = translator.translate('STOPP' , dest=lang)
            stop =[translated_stop.text.lower()]
            print(stop)
            translated_forward = translator.translate('FRAMÅT' , dest=lang)
            forward =[translated_forward.text.lower()]
            print(forward)
            translated_backward = translator.translate('TILLBAKA' , dest=lang)
            backward =[translated_backward.text.lower()]
            print(backward)
            translated_dance = translator.translate('DANCE' , dest=lang)
            dance =[translated_dance.text.lower()]
            print(dance)
            translated_right = translator.translate('HÖGER' , dest=lang)
            right =[translated_right.text.lower()]
            print(right)
            translated_left = translator.translate('VÄNSTER' , dest=lang)
            left =[translated_left.text.lower()]
            print(left)

            stoping = True
            if left[0] in message:
                message = 'left'
                stoping = False
                break
                #motion = PushF, LiftLE, DownLE, ForwardLE
            elif right[0] in message: 
                message = 'right'
                stoping = False
                break
                #motion = PushF, LiftRI, DownRI, ForwardRI
            elif forward[0] in message:
                stoping = False
                message = 'forward' 
                break
                #motion = PushF, LiftF, DownF, ForwardF
            elif backward[0] in message:
                stoping = False 
                message = 'backward'
                break
                #motion = PushF, LiftBW, DownBW, ForwardBW
            elif dance[0] in message:
                message = 'dance'
            
        message = 'I am walking' + ' ' + message
        translated = translator.translate(message , dest=lang)
        mytext = translated.text 
        print(mytext)
        language = lang
        myobj = gTTS(text=mytext, lang=language, slow=False) 
        myobj.save("welcome.mp3") 
        os.system("mpg321 -q welcome.mp3")  
        if message == 'dance':
            DanceStar()
            print("dance")
        while (stoping == False):
            while (1): 
                print("alright im here")
                #move(motion[0],motion[1],motion[2],motion[3])
                print("Recording Message")
                guess = recognize_speech_from_mic(recognizer, microphone,lang)
                print(guess)
                if guess["transcription"]:
                    break
                if not guess["success"]:
                    #move(motion[0],motion[1],motion[2],motion[3])
                    print("I didn't catch that. What did you say?\n")
                    break
                # if there was an error, stop
            if guess["error"]:
                print("ERROR: {}".format(guess["error"]))
                #move(motion[0],motion[1],motion[2],motion[3])
                break
            print("You said: {}".format(guess["transcription"]))
            message = guess["transcription"].lower() 
            if stop[0] in message: 
                message = 'I am stopping'
                translated = translator.translate(message , dest=lang)
                mytext = translated.text 
                language = lang
                myobj = gTTS(text=mytext, lang=language, slow=False) 
                myobj.save("welcome.mp3") 
                os.system("mpg321 -q welcome.mp3")   
                stoping = True     
    else:
        print("No matching words")


if __name__ == "__main__":
    #Standing up and storing values for motions
    #Stand_up()
    #PushF, LiftF, DownF, ForwardF, LiftBW, DownBW, ForwardBW, LiftLE, DownLE, ForwardLE, LiftRI, DownRI, ForwardRI, LiftTactile = CalculationMotions()
    motion_speech('en', 'Rebecca ')



     

