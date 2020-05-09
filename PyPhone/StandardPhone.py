import pygame
import config.config as config
import sys

def init(self):
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
    self._submitInput = pygame.K_KP_MULTIPLY
    self._closeInput = pygame.K_KP_PLUS

def update(self):
    # Pygame input
    for event in pygame.event.get():
        checkClosed(self, event)
        checkSubmit(self, event)
        checkNumbers(self, event)
        if event.type == pygame.QUIT:
            sys.exit(0)

def checkNumbers(self, event):
    if event.type == pygame.KEYDOWN:
        index = 0
        for i in self._input:
            if event.key == i:
                self._soundHandler.playRandTouchSound()
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
            self._inputBuffer = []
            self._soundHandler.playSound(config.DATA_AUDIO_MISC_PATH.joinpath('tonaliteDef.wav'), loop=True)

def checkSubmit(self, event):
    # Add conditions
    if event.type == pygame.KEYDOWN and event.key == self._submitInput:
        self._soundHandler.playRandTouchSound()
        self.submit()