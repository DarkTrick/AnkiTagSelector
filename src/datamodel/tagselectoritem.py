from .tagselectoritembaseinterface import TagSelectorItemBaseInterface

class TagSelectorItem(TagSelectorItemBaseInterface):
    """ - dataset of one Item within the list of selectable items
     - savable

     - every data, that should be available for each item goes here"""

    def __init__(self, tagsString = ""):
        # currently we have only one element here, but it might get more
        self.tagsString = tagsString

    def setTagsString(self, stringValue ):
        self.tagsString= stringValue

    def getTagsString(self) -> str:
        return self.tagsString

    def toString(self) -> str:
        return self.getTagsString()
