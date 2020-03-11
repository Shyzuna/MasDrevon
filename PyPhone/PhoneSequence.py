from PyPhone.SequenceElement import SequenceElement
from threading import Thread
import logging

class PhoneSequence(Thread):
    def __init__(self, seqFile):
        Thread.__init__(self)
        self._currentElement = 0
        self._seqElements = []
        self._seqFile = seqFile
        self._logger = logging.getLogger(__name__)

    def loadSeqFile(self):
        self._logger.info('Loading sequence {}'.format(str(self._seqFile)))

    def run(self):
        pass