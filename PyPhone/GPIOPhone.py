from gpiozero import Button
import config.config as config


def init(self):
    self._input = [
        Button(20),
        Button(21),
        Button(26),
        Button(19),
        Button(13),
        Button(6),
        Button(5),
        Button(22),
        Button(27),
        Button(17),
    ]
    self._oldInput = [False] * 10
    self._submitInput = Button(16)
    self._oldSubmitInput = False
    self._closeInput = Button(24)
    self._oldCloseInput = True

def update(self):
    checkClosed(self)
    checkSubmit(self)
    checkNumbers(self)

def checkNumbers(self):
    for i in range(0, 10):
        changed = self._oldInput[i] != self._input[i].is_pressed
        self._oldInput[i] = self._input[i].is_pressed
        if changed and self._oldInput[i]:
            self._inputBuffer.append(str(i))

def checkClosed(self):
    changed = self._oldCloseInput != self._closeInput.is_pressed
    self._oldCloseInput = self._closeInput.is_pressed
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
    # Add conditions
    changed = self._oldSubmitInput != self._submitInput.is_pressed
    self._oldSubmitInput = self._submitInput.is_pressed
    if changed and self._oldSubmitInput:
        self.submit()