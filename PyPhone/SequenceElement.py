from PyPhone.SequenceAction import SequenceAction
import config.config as config


class SequenceElement(object):
    def __init__(self, action, index, parent, seqNum, args=None):
        self._action = action
        self._args = args
        self._index = index
        self._parent = parent
        self._actionRunning = False
        self._actionDone = False
        self._seqNum = seqNum

        self._choices = {}
        self._lastChoice = None
        self._currentChoice = None
        self._currentIndex = 0
        self._oldIndex = -1

        self._waitCounter = 0

    def displayLocalCurrent(self):
        return '{}:{}'.format(self._action, self._args)
        if self._action == SequenceAction.choice:
            pass
        else:
            return '{}:{}'.format(self._action, self._args)

    def addChoicesOptions(self, num):
        if num not in self._choices:
            self._choices[num] = []
            self._lastChoice = num

    def addSeqElement(self, seq):
        self._choices[self._lastChoice].append(seq)
        seq.setParent(self)

    def setParent(self, parent):
        self._parent = parent

    def display(self, offset):
        print("{} {}{}:{}".format(self._index, ' ' * offset * 4, self._action.value[0], self._args))
        if self._action == SequenceAction.choice:
            for choiceVal, seqChoice in self._choices.items():
                print("{}{}:".format(' ' * (offset + 1) * 4, choiceVal))
                for seqElem in seqChoice:
                    seqElem.display(offset + 1)

    def doOneShootAction(self, pyphone):
        if self._action == SequenceAction.read:
            pyphone.getSoundHandler().playSound(config.DATA_AUDIO_BASE_PATH.joinpath(str(self._seqNum)).joinpath('{}.wav'.format(self._args)), startNow=True, callback=self.setActionDone)
        elif self._action == SequenceAction.record:
            # TODO
            self._actionDone = True
        elif self._action == SequenceAction.jump:
            # TODO
            self._actionDone = True

    def setActionDone(self):
        self._actionDone = True

    def submitChoice(self, val):
        # TODO
        pass

    def update(self, pyphone, deltaTime):
        if self._action == SequenceAction.choice:
            # TODO
            self._actionRunning = True
            self._actionDone = True
        elif self._action == SequenceAction.wait:
            self._actionRunning = True
            self._waitCounter += deltaTime
            if self._waitCounter >= int(self._args):
                self._actionDone = True
        elif not self._actionRunning:
            self._actionRunning = True
            self.doOneShootAction(pyphone)
        return self._actionDone
