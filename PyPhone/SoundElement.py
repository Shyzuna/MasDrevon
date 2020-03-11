from pathlib import Path
import config.config as config
import sounddevice as sd
import soundfile as sf


class SoundElement(object):
    def __init__(self, path, loop, callback):
        self._loop = loop
        self._callback = callback
        self._path = path

        self._currentAudio = sf.read(str(self._path))

    def playSound(self):
        sd.play(self._currentAudio[0], self._currentAudio[1])
        sd.play(self._currentAudio[0], self._currentAudio[1])

    def isLooping(self):
        return self._loop

    def soundEnded(self):
        print('Sound ended')
        if self._callback is not None:
            self._callback()