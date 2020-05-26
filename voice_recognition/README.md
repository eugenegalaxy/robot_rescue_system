This readme goes step by step through what you need for using the speachrec
ognition software for DNS

The program consist of 3 modules:
1. The main "VoiceRecognition" program which is executed once the voice recognition should be initialized.
2. The second is an add-on module for offline speech recognition and is called "OfflineVoice"
3. Last, we have a module which is checking the connection to the internet.

If the program is assumed to sorely run online, module 2-3 can be dissregarded and the functions shall be commented out in module 1.

Setting up mic and speakers: 
follow:
https://developers.google.com/assistant/sdk/guides/library/python/audio/embed

Instalation:

#### Make sure we have up-to-date versions of pip, setuptools and wheel ####
python2 -m pip install --upgrade pip setuptools wheel
python2 -m pip install --upgrade pip setuptools wheel

The main program is using several libraries which shall be installed before usage:

For gTTS (Google Text-to-Speech):
For Python2
python2 -m pip install gTTS
For Python3
python3 -m pip install gTTS
Quick Install
pip install gTTS


For speech_recognition (Library for several speach recognition engines and APIs, both online and offline):
For Python2
python2 -m pip install SpeechRecognition
For Python3
python3 -m pip install SpeechRecognition
Quick Install
pip install SpeechRecognition

For googletrans (API for translating texts from one language to another):
For Python2
python2 -m pip install googletrans
For Python3
python3 -m pip install googletrans
Quick Install
pip install googletrans

For PyAudio (Across-platform audio input/output stream library):
For Python2
python2 -m pip install PyAudio
For Python3
python3 -m pip install PyAudio
Quick Install
pip install PyAudio

For mpyg321 (Allows you to easily play mp3 sounds in python,):
sudo apt-get install mpg321

##### For checking internet ######

For checking the connectivity to internet the urllib is used and installed by 
Quick Install
pip install urllib3
Alternative:
git clone git://github.com/urllib3/urllib3.git
cd urllib3
python setup.py install 


#### For offline speech recognition ####
sudo apt-get install libpulse-dev
##Not sure if this is needed ###
snap install pulseaudio
sudo apt install pulseaudio-equalizer
################################
sudo apt-get install -y swig
python2 -m pip install --upgrade pocketsphinx
python3 -m pip install --upgrade pocketsphinx






##################### Speed up ######################
This step is not nssesary, but you can edit the pre-set values in speech_recognition to modify the "Recognize" voice part and also speed it up so there is less delays 
EDDIT __init__.py file located into the installed speech_recognition. Find path (possibly usr/local/lib/python3.6/dist-packages/speech_recognition)
Find class Recognizer 
Edit values such as

self.energy_threshold = NUMBER 
###minimum audio energy to consider for recording -- Depends on placement of mic and how much backround noice you expect, set NUMBER to 1000 if you expect to be much noice but mic close to user, otherwise use the already set value of 300. Play around to find the most optimal energy threshold for you!####
self.dynamic_energy_threshold = True
self.dynamic_energy_adjustment_damping = 0.15
self.dynamic_energy_ratio = 1.5
###these three lines dynamically adjust the energy threshold using asymmetric weighted average####
self.pause_threshold = 0.8  
### seconds of non-speaking audio before a phrase is considered complete ###
self.operation_timeout = None  
### seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout set to a number to make sure the it somtimes times out and start a new recordning###
self.phrase_threshold = 0.3  
### minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops), lower values can be used if you expect short anwers ###
self.non_speaking_duration = 0.5  
### seconds of non-speaking audio to keep on both sides of the recording ####


Tested parameters which react faster then the already set::
self.energy_threshold = 1000
self.dynamic_energy_threshold = True
self.dynamic_energy_adjustment_damping = 0.15
self.dynamic_energy_ratio = 1.5
self.phrase_threshold = 0.3  
self.pause_threshold = 0.3  
self.operation_timeout = 0.5  
self.non_speaking_duration = 0.3
