import sounddevice as sd
import soundfile as sf
from pathlib import Path
import config.config as config
from PyPhone.SoundElement import SoundElement
import logging
import random

# redundant code
# maybe play dial sound and touch in separate channel + touch sound / touch should not work on specific times
# Improve error handling


class SoundHandler(object):
    def __init__(self, pyphone):
        self._pyphone = pyphone
        self._currentStream = None
        self._sampleRate = 44100
        self._currentSound = None
        self._soundQueue = []
        self._recordMode = False
        self._recordPath = None
        self._recordCallback = None
        self._recordNum = None
        self._reservedCustomRecord = list(range(9999999000, 10000000000))
        self._record = None
        self._baseTouchSounds = [
            SoundElement(config.DATA_AUDIO_MISC_PATH.joinpath('touch0.wav'), False, None),
            SoundElement(config.DATA_AUDIO_MISC_PATH.joinpath('touch1.wav'), False, None),
            SoundElement(config.DATA_AUDIO_MISC_PATH.joinpath('touch2.wav'), False, None),
        ]
        self._logger = logging.getLogger(__name__)
        self.checkCustomReservedRecord()

    def checkCustomReservedRecord(self):
        self._logger.info('Checking reserved record names...')
        for p in config.DATA_AUDIO_CUSTOM_PATH.iterdir():
            if p.is_file():
                try:
                    self._reservedCustomRecord.remove(int(p.stem))
                except:
                    self._logger.warning('Wrong file in custom audio path : {}'.format(p.name))


    def playRandTouchSound(self):
        randS = self._baseTouchSounds[random.randint(0, len(self._baseTouchSounds) - 1)]
        self.stopCurrentSound()
        self._logger.debug('Touch sound playing')
        self._currentSound = randS
        self._currentSound.playSound()
        self._currentStream = sd.get_stream()

    def playSound(self, path, loop=False, startNow=True, callback=None):
        # CARE CALLBACK WITH PLAY SOUND !
        try:
            se = SoundElement(path, loop, callback)
        except:
            self._logger.error('Error while reading file')
            return
        # Could be better + check stop on stream
        if self._currentSound is None:
            self._logger.debug('Sound {} playing'.format(path))
            self._currentSound = se
            self._currentSound.playSound()
            self._currentStream = sd.get_stream()
        else:
            if startNow:
                self._logger.debug('Sound {} playing'.format(path))
                self.stopCurrentSound()
                # change sound
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
            self._currentSound.soundEnded()
            self._currentSound = None

    def updateSound(self):
        if self._currentStream is not None:
            if self._recordMode:
                if not self._currentStream.active:
                    # save sound
                    with sf.SoundFile(self._recordPath, 'x', samplerate=self._sampleRate, channels=2) as f:
                        f.write(self._record)
                    self._pyphone.addCustomSequence(self._recordNum)
                    self._record = None
                    self._currentStream = None
                    self._recordMode = False
                    self._recordNum = None
                    if self._recordCallback is not None:
                        self._recordCallback()
                        self._recordCallback = None
            else:
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

    def generateRecordPath(self):
        r = random.randint(0, len(self._reservedCustomRecord))
        self._recordNum = self._reservedCustomRecord[r]
        self._reservedCustomRecord.remove(self._recordNum)
        self._logger.info('Genrated record path : {}'.format(self._recordNum))
        return config.DATA_AUDIO_CUSTOM_PATH.joinpath('{}.wav'.format(self._recordNum))

    def recordSound(self, path=None, duration=5, callback=None):
        if not self._recordMode:
            self._logger.debug('Recording sound {} for {} s'.format(path, duration))
            if self._currentSound is not None:
                self.stopCurrentSound()
            if path is None:
                path = self.generateRecordPath()
            self._recordPath = path
            self._recordMode = True
            self._record = sd.rec(int(duration * self._sampleRate), samplerate=self._sampleRate, channels=2)
            self._currentStream = sd.get_stream()
            self._recordCallback = callback

