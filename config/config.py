from pathlib import Path

DATA_PATH = Path.cwd().joinpath('data')

DATA_AUDIO_CUSTOM_PATH = DATA_PATH.joinpath('audio').joinpath('custom')
DATA_AUDIO_BASE_PATH = DATA_PATH.joinpath('audio').joinpath('base')
DATA_AUDIO_SEQ_PATH = DATA_PATH.joinpath('sequence')
