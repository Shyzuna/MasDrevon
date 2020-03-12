from gpiozero import Button
import config.config as config


def init(self):
    self._input = [
        20,
        21,
        26,
        19,
        13,
        6,
        5,
        22,
        27,
        17,
    ]
    self._oldInput = [False] * 10
    self._submitInput = 16
    self._oldSubmitInput = False
    self._closeInput = 24
    self._oldCloseInput = True

def update(self):
    checkClosed(self)
    checkSubmit(self)
    checkNumbers(self)

def checkNumbers(self):
    pass

def checkClosed(self):
    closeIn = Button(self._closeInput)
    changed = self._oldCloseInput != closeIn.is_pressed
    self._oldCloseInput = closeIn.is_pressed
    if changed:
        self._closed = self._oldCloseInput
        if self._closed:
            self._pending = True
            self._logger.info('Phone closed')
            self.resetOnClosing()
        else:
            self._logger.info('Phone open')
            self._inputBuffer = []
            self._soundHandler.playSound(config.DATA_AUDIO_MISC_PATH.joinpath('tonaliteDef.wav'), loop=True)

def checkSubmit(self):
    pass