from PyPhone.SequenceAction import SequenceAction

class SequenceElement(object):
    def __init__(self, action, args=None):
        self._action = action
        self._choices = {}
        self._args = args

    def addChoicesOptions(self, num, seqElem):
        self._choices[num] = seqElem

    def doAction(self):
        if self._action == SequenceAction.READ:
            pass
        elif self._action == SequenceAction.WAIT:
            pass
        elif self._action == SequenceAction.CHOICE:
            pass
        elif self._action == SequenceAction.RECORD:
            pass
