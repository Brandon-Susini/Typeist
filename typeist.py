import subprocess,sys,os
import speech_recognition as sr
import pyttsx3, asyncio
import keyboard
from scamp import *
import warnings
warnings.filterwarnings("ignore")
s = Session()
ready_sound = s.new_part("Ocarina 2")
"""
keyboard.press_and_release('shift+s, space')


keyboard.add_hotkey('ctrl+shift+a', print, args=('triggered', 'hotkey'))

# Press PAGE UP then PAGE DOWN to type "foobar".
keyboard.add_hotkey('page up, page down', lambda: keyboard.write('foobar'))

# Blocks until you press esc.
keyboard.wait('esc')

# Record events until 'esc' is pressed.
recorded = keyboard.record(until='esc')
# Then replay back at three times the speed.
keyboard.play(recorded, speed_factor=3)

# Type @@ then press space to replace with abbreviation.
keyboard.add_abbreviation('@@', 'my.long.email@example.com')

# Block forever, like `while True`.
keyboard.wait()
"""


responses = {
    'still_talking': ["Was that all?", "Anything else?", "Got it."]
}
engine = pyttsx3.init('sapi5')   #Only use sapi 5 if it is Windows 10
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
#Initialize Recognizer Instance global
recognizer = None
#Initialize mic global
microphone = None

async def speak(audio):
    engine.say(audio)     #Start the actual speech
    engine.runAndWait() #Start talking and wait until after sentence is finished

async def listen(recog, mic):
    print("Began Listening")
    #Begin listening with mic as our source microphone
    with mic as source:
        recog.adjust_for_ambient_noise(mic,3)
        print("Listening...")
        ready_sound.play_note(84,0.5,0.1)
        #r.pause_threshold = 1
        audio = recog.listen(source)
    try:
        print("Recognizing...")
        query = recog.recognize_google(audio, language='en-us')
        outputFile = open("output.txt", "a")
        outputFile.write("\n" + query)
        keyboard.write(query)
        print(f"User said: {query.lower()}\n")
        return query
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return ""
    except sr.RequestError:
        print ("Could not request results from Google Speech Recognition service")
        return ""
    except Exception as e:
        print(e)
        return ""


async def takeCommand(active):
    query = await listen()
    print(f"Take command recieved command:  '{query}'")


async def start_listening(r,m):
    done = False
    while(not done):
        query = await listen(r,m)
        if(query != ""):
            print("User said: < " + query +" > ")
            if("quit" in query):
                return

        
async def main():
    print(os.environ.get('Path'))
    print("Main ran")
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=3)
    debug = 0
    if(debug >0):
        for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
            if(debug > 1):
                print("Microphone (" +str(i) +"): " + microphone_name )
            if "CABLE" in microphone_name:
                print("Microphone (" +str(i) +"): " + microphone_name )
    
    recognizer.pause_threshold = 0.5
    #path_opener.openPath()
    await start_listening(recognizer, microphone)


print("Program Started")
asyncio.run(main())

