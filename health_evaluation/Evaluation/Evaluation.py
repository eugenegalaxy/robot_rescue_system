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
from VoiceRecognition import *
import pyaudio
import logging



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
    translator = Translator()
    if Connection == False and fName is None:
        return
    else:
        for x in range(0,3):
            x = x+1
            if Connection == True:
                translated = translator.translate('' + phrase, dest=lang)
                mytext = translated.text 
                language = lang
                myobj = gTTS(text=mytext, lang=language, slow=False) 
                myobj.save("welcome.mp3") 
                os.system("mpg321 -q welcome.mp3")
            elif Connection == False:
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
            v_score = 3           
            recieve = repete_three('Please avoid moving your head. This can cause spinal cord injuries. Please try to answer the following questions as concisely as you can. Can you open your eyes and see your surroundings?',lang,('yes','no'),'eyes.mp3')
            if recieve[1] == True:                         
                e_score = 4
        

            v_score = verbal_response(lang, name, day, accident, place)
            v_score = v_score[0]
            m_score = motor_response(lang, name)
            m_score = m_score[0]
            report = evaluation(lang, name)
            report = report[0]
        else:
            return 'I have found ' + '' + name + ' The victim is awake and responding. But can not communicate.'


    else:    
        recieve = repete_three('' + name + ' wake up. Can you hear me?', lang, ('yes','no'),'wakeup.mp3',)
        guess = recieve[0]
        if guess["transcription"]:
            recieve = repete_three('Do you understand me?', lang , ('yes','no'),'understand.mp3')
            if recieve[1] == True:

            
                v_score = 3        
                recieve = repete_three('Please avoid moving your head. This can cause spinal cord injuries. Please try to answer the following questions as concisely as you can. Can you open your eyes and see your surroundings?',lang,('yes','no'),'eyes.mp3')
                if recieve[1] == True:                         
                    e_score = 3


                v_score = verbal_response(lang, name, day, accident, place)
                v_score = v_score[0]
                m_score = motor_response(lang, name)
                m_score = m_score[0]
                report = evaluation(lang, name)
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
    Connection = CheckingConnectionToGoogle()
    if Connection == True:
        print(Connection, "Connected")
    elif Connection == False:
        print("Connection lost")
    recieve = repete_three('Can you remember your name?',lang, ('yes','no'),'name.mp3') 
    if recieve[1] == True:
        recieve = repete_three('What is your name?',lang,(name,name),'whatName.mp3')
        guess = recieve[0]
        if guess["transcription"]:
            recieve = repete_three('What day of the week is today?',lang, (day,day),'day.mp3')
            if recieve[1] == True:
                recieve = repete_three('What natural disaster has happend recently?',lang,(accident,accident),'accident.mp3')
                if recieve[1] == True:
                    recieve = repete_three('where are we right now?', lang,(place,place),'place.mp3')
                    if recieve[1] == True:
                        score = 5
                    else:
                        score = 4
                else:
                    score = 4
            else:
                score = 4        
        

                      
    return score


def motor_response(lang,name):

    recieve = repete_three('Are you able to put your tongue out, and put it back into your mouth again?', lang,('yes','no'), 'motor.mp3')
    if recieve[1] == True:
        score = 6
    elif recieve[2] == True:
        score = 1
    else:
        score = 0
    return score

def evaluation(lang, name):
    Connection = CheckingConnectionToGoogle()
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
    if recieve[1] == True:
        text_trapped = 'I have found ' + '' + name + '. ' + '' + gender + ' is trapped.'
    elif recieve[2] == True:
        text_trapped = 'I have found ' + '' + name + '. ' + '' + gender +' is not trapped.'
    else:
        text_trapped = 'I have found ' + '' + name + '. I do not know if ' + '' + gender + ' is trapped or not.'
    recieve = repete_three('Can you move all your limbs?',lang,('yes','no'),'move.mp3')
    if recieve[1] == True:
        text_limbsmoving = '' + gender + ' can move all of the lims.'
    if recieve[2] == True:
        recive = repete_three('Which is the limb that you can not move it?', lang,('arm','leg'),'limb.mp3')
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
    if recieve[1] == True:
        recieve= repete_three('Where is the source of blood?',lang,('head','abdomen'),'bloodsource.mp3')
        if recieve[1] == True: 
            text_bleed = '' + gender + ' is bleeding on the head.'
        elif recieve[2] == True:
            text_bleed = '' + name + ' is bleeding on abdominal area.'
    elif recieve[2]:
        text_bleed = '' + gender + ' is not bleeding externally.'
    recieve = repete_three('Do you feel severe pain?',lang,('yes','no'),'pain.mp3')
    if recieve[1] == True:
        text_pain = '' + gender + ' feels sever pain.'
        recieve = repete_three('Where is the source of pain?',lang,('head','stomach'), 'painsource.mp3')
        if recieve[1] == True:
            text_pain = '' + gender + ' has severe headache.'
        elif recieve[2] == True:
            text_pain = '' + gender + ' feels severe abdominal pain.'
    elif recieve[2] == True:
        text_pain = '' + gender + ' does not feel severe pain.'
    oral_report = '' + text_trapped + '' + text_limb + '' + text_limbsmoving + '' + text_feel + '' + text_bleed + '' + text_pain
    print(oral_report)
    if Connection is True:
        recieve = repete_three('' + oral_report + ' Do you confirm?',lang,('yes','no'),None)
        if recieve is not None:
            if recieve[1] == True:
                oral_report = '' + oral_report + ' Victim confirmed.' 

    return oral_report


if __name__ == "__main__":                                   
    a = eye_opening('da','Dariush', 'sunday', 'earthquake', 'home')

