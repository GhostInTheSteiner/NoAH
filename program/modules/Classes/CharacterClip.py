import os


class CharacterClip:
    __fadeTime = 0
    __duration = 0
    __imagePath = ""



    def __init__(self, fadeTime, duration, imagePath):
        self.__fadeTime = fadeTime
        self.__duration = duration
        self.__imagePath = imagePath

        self.ffmpegPath = os.path.dirname(__file__ + "../../resources/ffmpeg/ffmpeg")



    def increaseDuration(self, appendedSeconds):
        self.__duration += appendedSeconds

    def __fadeIn(self):
        NotImplemented

    def __fadeOut(self):
        NotImplemented

    def __show(self):
        NotImplemented