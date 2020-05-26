import speech_recognition as sr

def OfflineVoice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("say something")
        audio = r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        recog = r.recognize_sphinx(audio)  
        print(recog)
        print("Sphinx thinks you said '" + recog + "'")  
        return recog
    except sr.UnknownValueError:  
        print("Sphinx could not understand audio")  
    except sr.RequestError as e:  
        print("Sphinx error; {0}".format(e))
    

