from enum import Enum


class SequenceAction(Enum):
    READ = 'read',
    CHOICE = 'choice',
    WAIT = 'wait',
    RECORD = 'record'
