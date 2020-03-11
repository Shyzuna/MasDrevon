from PyPhone.SequenceElement import SequenceElement
import logging
from PyPhone.SequenceAction import SequenceAction
from PyPhone.SequenceElement import SequenceElement
import re

class PhoneSequence(object):
    def __init__(self, seqFile):
        self._currentElement = 0
        self._seqElements = []
        self._seqFile = seqFile
        self._logger = logging.getLogger(__name__)

    def loadSeqFile(self):
        self._logger.info('Loading sequence {}'.format(str(self._seqFile)))
        content = []
        with open(str(self._seqFile)) as f:
            content = f.readlines()
        content = [line.strip() for line in content]
        lastAction = None
        regex = '^(' + '|'.join([e.value[0] for e in SequenceAction]) + '):?(.*)?'
        for line in content:
            #elements = line.split(':')
            res = re.search(regex, line)
            print(line)
            if res:
                print('match')
                print(res.group(1))
                print(res.group(0))
                print(res.group(2))
                # care cast exception
                lastAction = SequenceElement(SequenceAction[res.group(1)], res.group(2))

    def start(self):
        self._logger.info('Starting sequence {}'.format(str(self._seqFile)))

    def stop(self):
        self._logger.info('Stopping sequence {}'.format(str(self._seqFile)))

    def update(self):
        pass