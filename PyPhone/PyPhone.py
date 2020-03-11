from pathlib import Path
import config.config as config
import logging
import time
from PyPhone.SoundHandler import SoundHandler
from pathlib import Path


class PyPhone(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info('Starting PyPhone !')
        self._soundHandler = SoundHandler()

    def run(self):
        self._soundHandler.playSound(config.DATA_AUDIO_MISC_PATH.joinpath('tonaliteDef.wav'), loop=True, callback=lambda:print('tutu'))
        while True:
            self._soundHandler.updateSound()
