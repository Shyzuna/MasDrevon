import sounddevice as sd
import soundfile as sf
from pathlib import Path
import config.config as config


class PyPhone(object):
    def __init__(self):
        """sound = config.DATA_AUDIO_BASE_PATH.joinpath('9999999999').joinpath('debut.wav')
        data, fs = sf.read(str(sound))
        sd.play(data, fs)
        status = sd.wait()"""
