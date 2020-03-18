from PyPhone.SequenceAction import SequenceAction
import config.config as config
import logging


class SequenceElement(object):
    def __init__(self, action, index, parent, seqNum, args=None):
        self._action = action
        self._logger = logging.getLogger(__name__)
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
            # TOFINISH
            pyphone.getSoundHandler().recordSound('TODO', callback=self.setActionDone)
            self._actionDone = True
        elif self._action == SequenceAction.jump:
            # Care not checking if int
            pyphone.getCurrentSequence().doJump(int(self._args), self)
            self._actionDone = True

    def resetElement(self):
        # Should not reset every time on jump !
        #print('Reset {}'.format(self.displayLocalCurrent()))
        self._lastChoice = None
        self._currentChoice = None  # Care
        self._currentIndex = 0  # Care
        self._oldIndex = -1
        self._actionRunning = False
        self._actionDone = False

    def getParent(self):
        return self._parent

    def setRecCurrentElementTo(self, element):
        for key, val in self._choices:
            index = 0
            for elem in val:
                if elem == element:
                    print('{} set Index to {}'.format(self.displayLocalCurrent(), index))
                    self._currentChoice = key
                    self._currentIndex = index
                    break
                index += 1
        self._parent.setRecCurrentElementTo(self)

    def setActionDone(self):
        self._actionDone = True

    def submitChoice(self, val):
        if self._action == SequenceAction.choice:
            if self._currentChoice is None:
                self._logger.info('Choosing value {}'. format(val))
                self._currentChoice = val
                if val in self._choices.keys():
                    self._logger.info('Choice element is : {}'.format(self._choices[val][self._currentIndex].displayLocalCurrent()))
                    self._choices[self._currentChoice][self._currentIndex].resetElement()
                elif '*' in self._choices.keys():
                    self._logger.info('Default choice element is : {}'.format(self._choices['*'][self._currentIndex].displayLocalCurrent()))
                    self._choices['*'][self._currentIndex].resetElement()
                else:
                    self._logger.warning('No cases provided for the current choice')
            elif self._currentChoice in self._choices.keys():
                self._logger.info('Transmitting choice value to child')
                self._choices[self._currentChoice][self._currentIndex].submitChoice(val)
            else:
                self._logger.warning('Cannot use submitted value')
        else:
            self._logger.warning('No choice val required.')

    def update(self, pyphone, deltaTime):
        if self._action == SequenceAction.choice:
            self._actionRunning = True
            if self._currentChoice is not None:
                if self._currentChoice in self._choices.keys():
                    if self._choices[self._currentChoice][self._currentIndex].update(pyphone, deltaTime):
                        self._currentIndex += 1
                        if self._currentIndex >= len(self._choices[self._currentChoice]):
                            self._logger.info('End of sub sequence {}'.format(self._currentChoice))
                            self._actionDone = True
                        else:
                            self._logger.info('Sub sequence progressing to next : {}'.format(
                                self._choices[self._currentChoice][self._currentIndex].displayLocalCurrent()))
                            self._choices[self._currentChoice][self._currentIndex].resetElement()
                elif '*' in self._choices.keys():
                    if self._choices['*'][self._currentIndex].update(pyphone, deltaTime):
                        self._currentIndex += 1
                        if self._currentIndex >= len(self._choices['*']):
                            self._logger.info('End of sub sequence default')
                            self._actionDone = True
                        else:
                            self._logger.info('Sub sequence progressing to next : {}'.format(
                                self._choices['*'][self._currentIndex].displayLocalCurrent()))
                            self._choices['*'][self._currentIndex].resetElement()
                else:
                    self._logger.warning('No default case provided -> Passing')
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
