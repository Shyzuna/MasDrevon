from enum import Enum


class SequenceAction(Enum):
    read = 'read',
    choice = 'choice',
    wait = 'wait',
    record = 'record',
    jump = 'jump',
