from PyPhone.SequenceElement import SequenceElement
import logging
from PyPhone.SequenceAction import SequenceAction
from PyPhone.SequenceElement import SequenceElement
import re
from pathlib import Path
import config.config as config

class PhoneSequence(object):
    def __init__(self, seqFile, customReadOnly=False):
        self._currentElement = 0
        self._seqElements = []
        self._globalSeqElements = []
        self._seqFile = seqFile
        self._seqNum = self._seqFile.stem if issubclass(type(self._seqFile), Path) else self._seqFile
        self._logger = logging.getLogger(__name__)
        self._currentIndex = 0
        self._jumped = False
        if customReadOnly:
            self._basePath = config.DATA_AUDIO_CUSTOM_PATH
            readInst = SequenceElement(SequenceAction.read, 0, self, self._seqNum, str(self._seqNum))
            self._seqElements.append(readInst)
            self._globalSeqElements.append(readInst)
        else:
            self._basePath = config.DATA_AUDIO_BASE_PATH.joinpath(str(self._seqNum))
            self.loadSeqFile()
        print('Base {}'.format(self._basePath))

    def loadSeqFile(self):
        # Improve this shit ? + Add error cases =O
        self._logger.info('Loading sequence {}'.format(str(self._seqFile)))
        content = []
        with open(str(self._seqFile)) as f:
            content = f.readlines()
        content = [line.replace('\n', '').replace('\t', '    ') for line in content]
        baseRegex = '^(\s*)(' + '|'.join([e.value[0] for e in SequenceAction]) + ')(:.*)?'
        choiceRegex = '^(\s*)(\d*|\*):(' + '|'.join([e.value[0] for e in SequenceAction]) + ')?(:.*)?'
        currentLevel = 0
        lineCounter = 0
        lastAction = None
        choicesLevel = {}
        for line in content:
            choiceVal = None
            res = re.search(baseRegex, line)
            res2 = re.search(choiceRegex, line)
            print(line)
            if res:
                #print('match base')
                space = res.group(1)
                action = res.group(2)
                arg = res.group(3)[1::] if res.group(3) is not None else None
                currentLevel = len(space) / 4
                #print(res.group(1))
                #print(res.group(2))
                #print(res.group(3))
                #print(currentLevel)
                lastAction = SequenceElement(SequenceAction[action], lineCounter, self, self._seqNum, arg)

                # If in choices list
                if currentLevel > 0:
                    choicesLevel[currentLevel - 1].addSeqElement(lastAction)
                else:
                    self._seqElements.append(lastAction)

                self._globalSeqElements.append(lastAction)

                # If action is choice
                if action == 'choice':
                    #print('adding choice')
                    choicesLevel[currentLevel] = lastAction

            elif res2:
                #print('match choice')
                space = res2.group(1)
                choiceVal = res2.group(2)
                action = res2.group(3)
                arg = res2.group(4)[1::] if res2.group(4) is not None else None
                currentLevel = len(space) / 4
                #print(res2.group(1))
                #print(res2.group(2))
                #print(res2.group(3))
                #print(res2.group(4))
                #print(currentLevel)
                if currentLevel > 0:
                    choicesLevel[currentLevel - 1].addChoicesOptions(choiceVal)
                    if action is not None:
                        lastAction = SequenceElement(SequenceAction[action], lineCounter, self, self._seqNum, arg)
                        self._globalSeqElements.append(lastAction)
                        choicesLevel[currentLevel - 1].addSeqElement(lastAction)
                        # If action is choice
                        if action == 'choice':
                            #print('adding choice')
                            choicesLevel[currentLevel] = lastAction
                else:
                    self._logger.error('Syntax error line {} : {}'.format(lineCounter, line))
                    return False

            else:
                self._logger.error('Syntax error line {} : {}'.format(lineCounter, line))
                return False
            lineCounter += 1
            #print('------------')
        """index = 0
        for elem in self._globalSeqElements:
            print('{} : {}'.format(index, elem.displayLocalCurrent()))
            index += 1"""
        return True

    def getBaseAudioPath(self):
        return self._basePath

    def doJump(self, val, element):
        if len(self._globalSeqElements) > val - 1 > -1:
            self._logger.info('Jumping to element : {}'.format(val))
            self._globalSeqElements[val - 1].getParent().setRecCurrentElementTo(self._globalSeqElements[val - 1])
            self._jumped = True
        else:
            self._logger.warning('Cannot Jump to {} -> Skipping'.format(val))
            element.setActionDone()

    def setRecCurrentElementTo(self, element):
        index = 0
        for elem in self._seqElements:
            if elem == element:
                print('{} set Index to {}'.format(__name__, index))
                self._currentIndex = index
                self._seqElements[index].resetElement()
                break
            index += 1

    def displaySeq(self):
        for seqElem in self._seqElements:
            seqElem.display(0)

    def submitChoice(self, val):
        self._seqElements[self._currentIndex].submitChoice(val)

    def start(self):
        self._logger.info('Starting sequence {}'.format(str(self._seqFile)))
        self._logger.info('First element : {}'.format(self._seqElements[self._currentIndex].displayLocalCurrent()))
        # Overkill ?
        for elem in self._globalSeqElements:
            elem.resetElement()

    def stop(self):
        self._logger.info('Stopping sequence {}'.format(str(self._seqFile)))

    def update(self, pyphone, deltaTime):
        if self._seqElements[self._currentIndex].update(pyphone, deltaTime):
            if not self._jumped:
                self._currentIndex += 1
                if self._currentIndex >= len(self._seqElements):
                    self._logger.info('End of sequence {}'.format(str(self._seqFile)))
                    return True
                else:
                    self._logger.info('Sequence progressing to next : {}'.format(
                        self._seqElements[self._currentIndex].displayLocalCurrent()))
                    self._seqElements[self._currentIndex].resetElement()
            else:
                self._jumped = False
        return False