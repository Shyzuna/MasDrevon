from enum import Enum


class SequenceAction(Enum):
    READ = 1,
    CHOICE = 2,
    WAIT = 3,
    RECORD = 4
