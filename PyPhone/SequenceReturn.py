from enum import Enum

class SequenceReturn(Enum):
    DONE = 0,
    NOTYET = 1,
    JUMPED = 2
