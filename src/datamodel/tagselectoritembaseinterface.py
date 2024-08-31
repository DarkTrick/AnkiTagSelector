class TagSelectorItemBaseInterface:
    """ defines functions, that should be implemented by derived classes
        to make sync between gui-datastructure and datastructure easier"""
    def _notYetImplementedException(self):
        raise Exception("implemented by derived class")

    def setTagsString(self, stringValue):
        self._notYetImplementedException()

    def getTagsString(self):
        self._notYetImplementedException()