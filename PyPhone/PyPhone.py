from pathlib import Path
import config.config as config
import logging
import time
from PyPhone.SoundHandler import SoundHandler
from pathlib import Path
from PyPhone.PhoneSequence import PhoneSequence
import os
from PyPhone.SequenceAction import SequenceAction

if config.INPUT_TYPE == 'STD':
    import PyPhone.StandardPhone as PhoneFunc
else:
    import PyPhone.GPIOPhone as PhoneFunc

# check pending and closing condition
# rename pending <-> dialing ?


class PyPhone(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info('Starting PyPhone !')
        self._soundHandler = SoundHandler()
        self._inputBuffer = []
        self._pending = True
        self._closed = True
        self._currentSequence = None

        # Automatically load sequences
        self._sequenceByNumber = {}
        self.loadAllSequences()

        self._currentSequence = self._sequenceByNumber['9999999999']
        self._currentSequence.start()

        self._calledNumber = None

        PhoneFunc.init(self)

    def getCurrentSequence(self):
        return self._currentSequence

    def getSoundHandler(self):
        return self._soundHandler

    def loadAllSequences(self):
        self._logger.info('Loading sequences...')
        for p in config.DATA_AUDIO_SEQ_PATH.iterdir():
            if p.is_file():
                self._logger.info('Loading sequence : {}'.format(p.name))
                self._sequenceByNumber[p.stem] = PhoneSequence(p.absolute())

    def checkBufferInput(self):
        if not self._closed and self._pending and len(self._inputBuffer) == 10:
            self._pending = False
            self._calledNumber = ''.join(self._inputBuffer)
            self._logger.info('Calling phone number : {}'.format(self._calledNumber))
            self._soundHandler.playSound(config.DATA_AUDIO_MISC_PATH.joinpath('compositionNum2.wav'), startNow=True, callback=self.checkCalledNumber)
            self._inputBuffer = []

    def checkCalledNumber(self):
        if self._calledNumber in self._sequenceByNumber.keys():
            self._logger.info('Phone number {} exists'.format(self._calledNumber))
            self._currentSequence = self._sequenceByNumber[self._calledNumber]
            self._currentSequence.loadSeqFile()
            self._currentSequence.start()
        else:
            self._logger.info('Phone number {} unknown'.format(self._calledNumber))
            self._soundHandler.playSound(config.DATA_AUDIO_MISC_PATH.joinpath('occupe.wav'), startNow=True, loop=True)

    def resetOnClosing(self):
        self._soundHandler.stopCurrentSound()
        self._inputBuffer = []
        if self._currentSequence is not None:
            self._currentSequence.stop()
            self._currentSequence = None

    def submit(self):
        self._logger.info('Submit')
        self._logger.info('Buffer number : {}'.format(self._inputBuffer))
        val = ''.join(self._inputBuffer)
        self._inputBuffer = []
        if self._currentSequence is not None:
            self._currentSequence.submitChoice(val)

    def run(self):
        oldTime = time.time()
        while True:
            deltaTime = time.time() - oldTime
            oldTime = time.time()
            self._soundHandler.updateSound()
            PhoneFunc.update(self)
            self.checkBufferInput()
            if self._currentSequence is not None:
                end = self._currentSequence.update(self, deltaTime)
                if end:
                    self._currentSequence = None
                    self._soundHandler.playSound(config.DATA_AUDIO_MISC_PATH.joinpath('occupe.wav'), startNow=True,
                                                 loop=True)
            time.sleep(0.1)
