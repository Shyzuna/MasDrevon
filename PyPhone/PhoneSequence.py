from PyPhone.SequenceElement import SequenceElement


class PhoneSequence(object):
    def __init__(self, seqFile):
        self._currentElement = 0
        self._seqElements = []
        self._seqFile = seqFile

    def loadSeqFile(self):
        pass