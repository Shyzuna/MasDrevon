import sounddevice as sd
import soundfile as sf
from pathlib import Path
import config.config as config
from PyPhone.SoundElement import SoundElement
import logging

# redundant code


class SoundHandler(object):
    def __init__(self):
        self._currentStream = None
        self._currentSound = None
        self._soundQueue = []
        self._logger = logging.getLogger(__name__)

    def playSound(self, path, loop=False, startNow=True, callback=None):
        se = SoundElement(path, loop, callback)
        # Could be better + check stop on stream
        if self._currentSound is None:
            self._logger.debug('Sound {} playing'.format(path))
            self._currentSound = se
            self._currentSound.playSound()
            self._currentStream = sd.get_stream()
        else:
            if startNow:
                self._logger.debug('Sound {} playing'.format(path))
                self._currentStream.stop()
                self._currentSound = se
                self._currentSound.playSound()
                self._currentStream = sd.get_stream()
            else:
                self._logger.debug('Sound {} in queue'.format(path))
                self._soundQueue.append(se)

    def stopCurrentSound(self):
        self._logger.debug('Stopping current sound')
        if self._currentStream is not None:
            self._currentStream.stop()
            self._currentSound = None

    def updateSound(self):
        if self._currentStream is not None:
            if not self._currentStream.active and self._currentSound is not None:
                self._currentSound.soundEnded()
                if self._currentSound.isLooping():
                    self._currentSound.playSound()
                    self._currentStream = sd.get_stream()
                elif len(self._soundQueue) > 0:
                    self._currentSound = self._soundQueue[0]
                    self._soundQueue.remove(self._currentSound)
                    self._currentSound.playSound()
                    self._currentStream = sd.get_stream()
                else:
                    self._currentStream = None
                    self._currentSound = None