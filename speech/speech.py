from gtts import gTTS
import os


class Speech:
    def __init__(self) -> None:
        pass
    def speak(self, Input):
        try:
            myobj = gTTS(text=Input, lang='en', slow=False, tld="us")
            filename = "./temp.mp3"
            myobj.save(filename)
            os.system("mpg123 " + filename)
            os.remove(filename)
        except:
            os.remove(filename)
