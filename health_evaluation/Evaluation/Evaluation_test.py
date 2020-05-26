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
from VoiceRecognition import *
#from ctypes import *
#from contextlib import contextmanager
import pyaudio
import logging
#import example


# ######for my errors###
# def reb_errore():
#     ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

#     def py_error_handler(filename, line, function, err, fmt):
#         pass

#     c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

#     @contextmanager
#     def noalsaerr():
#         asound = cdll.LoadLibrary('libasound.so')
#         asound.snd_lib_error_set_handler(c_error_handler)
#         yield
#         asound.snd_lib_error_set_handler(None)

#     with noalsaerr():
#         p = pyaudio.PyAudio()
#         stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)

def recorde(lang):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    print("Recording Message")

    if lang == 'da':
        guess = recognize_speech_from_mic(recognizer, microphone, 'da-DK')
    elif lang == 'sv':
        guess = recognize_speech_from_mic(recognizer, microphone, 'sv-SE')
    elif lang == 'ru':
        guess = recognize_speech_from_mic(recognizer, microphone, 'ru-RU')
    else :
        guess = recognize_speech_from_mic(recognizer, microphone, 'en-UK')
    return guess

def repete_three(phrase,lang,keyWord,fName=None):
    output_1 = False
    output_2 = False
    keyWord_1 = translate(keyWord[0],lang)
    keyWord_2 = translate(keyWord[1],lang)

    
    Connection = CheckingConnectionToGoogle()
    if isinstance(Connection,tuple):
        Connection = Connection[0]
    #reb_errore()
    translator = Translator()
    if Connection == False and fName is None:
        return
    else:
        for x in range(0,3):
            x = x+1
            if Connection == True:
                #print(Connection, "Connected")
                translated = translator.translate('' + phrase, dest=lang)
                mytext = translated.text 
                language = lang
                myobj = gTTS(text=mytext, lang=language, slow=False) 
                myobj.save("welcome.mp3") 
                os.system("mpg321 -q welcome.mp3")
            elif Connection == False:
                #print(Connection,"Connection lost")
                if fName is not None:
                    os.system("mpg321 -q {}".format(fName))

            guess = recorde(lang)
            if guess["transcription"]:
                message =  guess["transcription"].lower()
                if keyWord_1 in message:
                    output_1 = True
                if keyWord_2 in message:
                    output_2 = True
                
                if (output_1 == True) or (output_2 == True):
                    break
        
        print('Try number: {}'.format(x))
        if guess["transcription"]:
            conversation = 'Question:'+'' + phrase + 'Answer:' + '' + guess["transcription"]
        elif guess["error"]:
            conversation = 'Question:'+'' + phrase + 'Answer:' + '' + guess["error"]
        out = (guess, output_1, output_2, conversation)
        return out    



def translate(keyWord,lang):
    translator = Translator()
    Connection = CheckingConnectionToGoogle()
    if isinstance(Connection,tuple):
        Connection = Connection[0]
    if Connection == True:
        lang = lang
        translated_keyWord = translator.translate(keyWord , dest=lang)
        keyWord =translated_keyWord.text.lower()
    return keyWord



def eye_opening(lang, name, day, accident, place ):
    total = 0
    Connection = CheckingConnectionToGoogle()
    conversation = ['']
    if isinstance(Connection,tuple):
        Connection = Connection[0]
        #print(Connection, "I knew this")
    # if isinstance(Connection,tuple):
    #     Connection = Connection[0]
    # if Connection == True:
    #     print(Connection, "Connected")
    #     translated_yes = translator.translate('Yes' , dest=lang)
    #     wordYes =[translated_yes.text.lower()]
    #     translated_no = translator.translate('No' , dest=lang)
    #     wordNo =[translated_no.text.lower()]
    #     translated_danish = translator.translate('Danish' , dest=lang)
    #     wordDanish =[translated_danish.text.lower()]
    #     translated_swedish = translator.translate('Swedish' , dest=lang)
    #     wordSwedish =[translated_swedish.text.lower()]
    #     translated_russian = translator.translate('Russian' , dest=lang)
    #     wordRussian =[translated_russian.text.lower()]
    #     translated_english = translator.translate('English' , dest=lang)
    #     wordEnglish =[translated_english.text.lower()]
    # if lang == 'da':
    #     mothertongue = 'Danish'
    # elif lang == 'se':
    #     mothertongue = 'Swedish'
    # elif lang == 'ru':
    #     mothertongue = 'Russian'
    # else:
    #     mothertongue = 'English'
    # else:
    #     wordYes =['Yes']
    #     wordNo =['No']
    e_score = 0
    v_score = 0
    m_score = 0
    report = ''



    recieve = repete_three('Hello, I am here to help you. Can you hear me?', lang, ('yes', 'no'), 'hello.mp3')
    conversation.extend([recieve[3]])
    guess = recieve[0]
    if guess["transcription"]:
        recieve = repete_three('Do you understand me?', lang , ('yes','no'),'understand.mp3')
        conversation.extend([recieve[3]])
        if recieve[1] == True:
            # recieve = repete_three('Do you speakEnlish?', 'en',('yes','no'), None)
            # conversation.extend([recieve[3]])
            # if recieve[1] is not True:
            #     if Connection == True:
            #         recieve = repete_three('Please choose between the following languages: English, Danish, Swedish and Russian', lang, ('',''), None)
            #         conversation.extend([recieve[3]])
            #         guess = recieve[0]
            #         if guess["transcription"]:
            #             message = guess["transcription"].lower()
            #             print(message)
            #             if 'english' in message:
            #                 lang = 'en' 
            #             elif 'danish' in message:
            #                 lang = 'da' 
            #             elif 'swedish' in message:
            #                 lang = 'sv'
            #             elif 'russian' in message:
            #                 lang = 'ru'
            #             else:
            #                 os.system("mpg321 -q sorry2.mp3")  
            #                 return 'I have found ' + '' + name + '. The victim is awake and responding. But can not communicate.'
             #elif recieve[1] == True:
            #        lang = 'en'

            # guess = repete_three('I am a member of the search and rescue team. I am here to evaluate your condition and report it 
            v_score = 3           
            recieve = repete_three('Please avoid moving your head. This can cause spinal cord injuries. Please try to answer the following questions as concisely as you can. Can you open your eyes and see your surroundings?',lang,('yes','no'),'eyes.mp3')
            if recieve[1] == True:                         
                e_score = 4
        

            v_score = verbal_response(lang, name, day, accident, place)
            conversation.extend([v_score[1]])
            v_score = v_score[0]
            m_score = motor_response(lang, name)
            conversation.extend([m_score[1]])
            m_score = m_score[0]
            report = evaluation(lang, name)
            conversation.extend([report[1]])
            report = report[0]
        else:
            return 'I have found ' + '' + name + ' The victim is awake and responding. But can not communicate.'


    else:    
        recieve = repete_three('' + name + ' wake up. Can you hear me?', lang, ('yes','no'),'wakeup.mp3',)
        conversation.extend([recieve[3]])
        guess = recieve[0]
        #print(guess["transcription"])
        if guess["transcription"]:
            recieve = repete_three('Do you understand me?', lang , ('yes','no'),'understand.mp3')
            conversation.extend([recieve[3]])
            if recieve[1] == True:
                # recieve = repete_three('Do you speak English?','en',('yes','no'), 'english.mp3')
                # conversation.extend([recieve[3]])
                # if recieve[1] == True:
                    # if Connection == True:
                    #     recieve = repete_three('Please choose between the following languages: English, Danish, Swedish and Russian', 'en', ('',''), None)
                    #     conversation.extend([recieve[3]])
                    #     guess = recieve[0]
                    #     if guess["transcription"]:
                    #         message = guess["transcription"].lower()
                    #         print(message)
                    #         if 'english' in message:
                    #             lang = 'en' 
                    #         elif 'danish' in message:
                    #             lang = 'da' 
                    #         elif 'swedish' in message:
                    #             lang = 'sv'
                    #         elif 'russian' in message:
                    #             lang = 'ru'
                    #         else:
                    #             os.system("mpg321 -q sorry2.mp3")
                    #             return 'I have found ' + '' + name + '. The victim is awake and responding. But can not communicate.'
                #elif recieve[1] == True:
                #    lang = 'en'

            
                v_score = 3        
                recieve = repete_three('Please avoid moving your head. This can cause spinal cord injuries. Please try to answer the following questions as concisely as you can. Can you open your eyes and see your surroundings?',lang,('yes','no'),'eyes.mp3')
                conversation.extend([recieve[3]])
                if recieve[1] == True:                         
                    e_score = 3


                v_score = verbal_response(lang, name, day, accident, place)
                conversation.extend([v_score[1]])
                v_score = v_score[0]
                m_score = motor_response(lang, name)
                conversation.extend([m_score[1]])
                m_score = m_score[0]
                report = evaluation(lang, name)
                conversation.extend([report[1]])
                report = report[0]

            else:
                return 'I have found ' + '' + name + '. The victim is awake but not responding.' 
        if not guess["success"]:
            print("ERROR: {}".format(guess["error"]))
        else:
            return 'I have found ' + '' + name + '. The victim is not awake and responding.'
    total = e_score + v_score + m_score   
    print("v_score: {}".format(v_score))
    print("e_score: {}".format(e_score))
    print("m_score: {}".format(m_score))
    print("Total score:{}".format(total))

    return [v_score, e_score, m_score,total, report, conversation]


def verbal_response(lang, name, day, accident, place):
    score = 3
    conversation = ['']
    Connection = CheckingConnectionToGoogle()
    if Connection == True:
        print(Connection, "Connected")
    elif Connection == False:
        print("Connection lost")
    recieve = repete_three('Can you remember your name?',lang, ('yes','no'),'name.mp3') 
    conversation.extend([recieve[3]])
    if recieve[1] == True:
        recieve = repete_three('What is your name?',lang,(name,name),'whatName.mp3')
        conversation.extend([recieve[3]])
        guess = recieve[0]
        if guess["transcription"]:
            recieve = repete_three('What day of the week is today?',lang, (day,day),'day.mp3')
            conversation.extend([recieve[3]])
            if recieve[1] == True:
                recieve = repete_three('What natural disaster has happend recently?',lang,(accident,accident),'accident.mp3')
                conversation.extend([recieve[3]])
                if recieve[1] == True:
                    recieve = repete_three('where are we right now?', lang,(place,place),'place.mp3')
                    conversation.extend([recieve[3]])
                    if recieve[1] == True:
                        score = 5
                    else:
                        score = 4
                else:
                    score = 4
            else:
                score = 4        
        

                      
    return score, conversation


def motor_response(lang,name):

    #Connection = CheckingConnectionToGoogle()
    conversation = ['']
    recieve = repete_three('Are you able to put your tongue out, and put it back into your mouth again?', lang,('yes','no'), 'motor.mp3')
    conversation.extend([recieve[3]])
    if recieve[1] == True:
        score = 6
    elif recieve[2] == True:
        score = 1
    else:
        score = 0
    return score,conversation

def evaluation(lang, name):
    Connection = CheckingConnectionToGoogle()
    conversation = []
    if name == '':
        name == translate('Unknow victim', lang)
    if name == 'rebecca':
        gender = translate('She',lang)
        gender_2 = translate('her',lang)
    else:
        gender = translate('He',lang)
        gender_2 = translate('his',lang)


    text_limb = ''
    text_trapped = ''
    text_limbsmoving = ''
    text_feel = ''
    text_bleed = ''
    text_pain = ''

    recieve = repete_three('Are you trapped?',lang,('no','yes'),'trapped.mp3')
    conversation.extend([recieve[3]])
    if recieve[1] == True:
        #print('Victim is trapped.')
        text_trapped = 'I have found ' + '' + name + '. ' + '' + gender + ' is trapped.'
    elif recieve[2] == True:
        #print('Victim is free.')
        text_trapped = 'I have found ' + '' + name + '. ' + '' + gender +' is not trapped.'
    else:
        text_trapped = 'I have found ' + '' + name + '. I do not know if ' + '' + gender + ' is trapped or not.'
    recieve = repete_three('Can you move all your limbs?',lang,('yes','no'),'move.mp3')
    conversation.extend([recieve[3]])
    if recieve[1] == True:
        text_limbsmoving = '' + gender + ' can move all of the lims.'
    if recieve[2] == True:
        recive = repete_three('Which is the limb that you can not move it?', lang,('arm','leg'),'limb.mp3')
        conversation.extend([recieve[3]])
        if recieve[1] == True or recive[2] == True:
            if recieve[1] == True and recieve[2] == False:
                text_limb = '' + gender + ' is not able to move ' + '' + gender_2 + ' arm.'
            elif recieve[2] == True and recieve[1] == False:
                text_limb = '' + gender + ' is not able to move ' + '' + gender_2 + ' leg.'
            elif recieve[1] == True and recieve[2] == True:
                text_limb = '' + gender + ' is not able to move any of the limbs.'
            recieve = repete_three('Can you still feel it?', lang,('yes','no'),'feel.mp3') 
            if recieve[1] == True and recieve[2] == False:
                        text_feel = 'But ' + '' + gender + ' can still feel it.'
            elif recieve[2] == True and recieve[1] == False:
                        text_feel = 'And ' + '' + gender + ' can not feel it.'
            elif recieve[1] == True and recieve[2] == True:
                text_feel = 'And ' + '' + gender + ' can not feel both.'
            else:
                text_feel = 'And I do not know if' + '' + gender + ' can feel it or not.'  
    else:
        text_limbsmoving = 'I do not know if ' + '' + gender + ' can move ' + '' + gender_2 + ' limbs or not.'
                            
    recieve = repete_three('Are you bleeding?', lang,('yes','no'),'bleeding.mp3')
    conversation.extend([recieve[3]])
    if recieve[1] == True:
        recieve= repete_three('Where is the source of blood?',lang,('head','abdomen'),'bloodsource.mp3')
        conversation.extend([recieve[3]])
        if recieve[1] == True: 
            #print("Victim is bleeding on the head.")
            text_bleed = '' + gender + ' is bleeding on the head.'
        elif recieve[2] == True:
            #print("Victim is bleeding on abdominal area.")
            text_bleed = '' + name + ' is bleeding on abdominal area.'
    elif recieve[2]:
        text_bleed = '' + gender + ' is not bleeding externally.'
    recieve = repete_three('Do you feel severe pain?',lang,('yes','no'),'pain.mp3')
    conversation.extend([recieve[3]])
    if recieve[1] == True:
        text_pain = '' + gender + ' feels sever pain.'
        recieve = repete_three('Where is the source of pain?',lang,('head','stomach'), 'painsource.mp3')
        conversation.extend([recieve[3]])
        if recieve[1] == True:
            #print("Victim has pain on the head.")
            text_pain = '' + gender + ' has severe headache.'
        elif recieve[2] == True:
            #print("Victim has pain on abdominal area.")
            text_pain = '' + gender + ' feels severe abdominal pain.'
    elif recieve[2] == True:
        #print("Victim doesn't feel sever pain.")
        text_pain = '' + gender + ' does not feel severe pain.'
    oral_report = '' + text_trapped + '' + text_limb + '' + text_limbsmoving + '' + text_feel + '' + text_bleed + '' + text_pain
    print(oral_report)
    if Connection is True:
        recieve = repete_three('' + oral_report + ' Do you confirm?',lang,('yes','no'),None)
        conversation.extend([recieve[3]])
        if recieve is not None:
            if recieve[1] == True:
                #print("The victim confirmed above")
                oral_report = '' + oral_report + ' Victim confirmed.' 

    return oral_report,conversation


if __name__ == "__main__":                                   
    a = eye_opening('da','Dariush', 'sunday', 'earthquake', 'home')
    path = os.path.dirname(os.path.abspath(__file__))
    local_path = "testing_evaluation/scenario_1.log"
    full_path = os.path.join(path, local_path)
    logging.basicConfig(filename = full_path,level=logging.DEBUG,format='%(asctime)s :: %(message)s')
    logging.info(a[5])
    print(a)