from pathlib import Path
import config.config as config
import logging
import time
from PyPhone.SoundHandler import SoundHandler
from pathlib import Path
import pygame
from PyPhone.PhoneSequence import PhoneSequence

# check pending and closing condition


class PyPhone(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info('Starting PyPhone !')
        self._soundHandler = SoundHandler()
        self._inputBuffer = []
        self._pending = True
        self._closed = True
        # Automatically load sequences
        self._sequenceByNumber = {
            '9999999999': PhoneSequence(config.DATA_AUDIO_SEQ_PATH.joinpath('9999999999.seq'))
        }
        self._calledNumber = None
        # tmp
        pygame.init()
        (width, height) = (300, 200)
        screen = pygame.display.set_mode((width, height))
        self._input = [
            pygame.K_KP0,
            pygame.K_KP1,
            pygame.K_KP2,
            pygame.K_KP3,
            pygame.K_KP4,
            pygame.K_KP5,
            pygame.K_KP6,
            pygame.K_KP7,
            pygame.K_KP8,
            pygame.K_KP9,
        ]
        self._submitInput = pygame.K_KP_ENTER
        self._closeInput = pygame.K_KP_PLUS

    def getInput(self):
        # using pygame atm
        for event in pygame.event.get():
            self.checkClosed(event)
            self.checkSubmit(event)
            if event.type == pygame.KEYDOWN:
                index = 0
                for i in self._input:
                    if event.key == i:
                        self._inputBuffer.append(str(index))
                        break
                    index += 1

    def checkClosed(self, event):
        if event.type == pygame.KEYDOWN and event.key == self._closeInput:
            self._closed = not self._closed
            if self._closed:
                self._pending = True
                self._logger.info('Phone closed')
                self.resetOnClosing()
            else:
                self._logger.info('Phone open')
                self._soundHandler.playSound(config.DATA_AUDIO_MISC_PATH.joinpath('tonaliteDef.wav'), loop=True)

    def checkSubmit(self, event):
        # Add conditions
        if event.type == pygame.KEYDOWN and event.key == self._submitInput:
            self.submit()

    def checkBufferInput(self):
        if not self._closed and self._pending and len(self._inputBuffer) == 10:
            self._pending = False
            self._calledNumber = ''.join(self._inputBuffer)
            self._logger.info('Calling phone number : {}'.format(self._calledNumber))
            self._soundHandler.playSound(config.DATA_AUDIO_MISC_PATH.joinpath('compositionNum2.wav'), startNow=True, callback=self.checkCalledNumber)

    def checkCalledNumber(self):
        if self._calledNumber in self._sequenceByNumber.keys():
            self._logger.info('Phone number {} exists'.format(self._calledNumber))
        else:
            self._logger.info('Phone number {} unknown'.format(self._calledNumber))
            self._soundHandler.playSound(config.DATA_AUDIO_MISC_PATH.joinpath('occupe.wav'), startNow=True, loop=True)

    def resetOnClosing(self):
        self._soundHandler.stopCurrentSound()
        self._inputBuffer = []

    def submit(self):
        self._logger.info('Submit')
        self._logger.info('Buffer number : {}'.format(self._inputBuffer))
        self._inputBuffer = []

    def run(self):
        while True:
            self._soundHandler.updateSound()
            self.getInput()
            #self.checkPending()
            #self.checkSubmit()
            self.checkBufferInput()
