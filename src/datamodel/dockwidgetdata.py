


from ..qthelper.qtimports import QtCore # Core for Signals; Gui for gui
from ..config import gDefaultTagSelectorSizeArea
from ..config import gDefaultTagSelectorSizeAreaHeight

import os # for default path of savefile
import pickle # for saving to fs

class DockWidgetData:
    """
    Datamodel for the dock widget we use to place the
    Tagselector
    """
    def __init__(self):
        self.position = QtCore.Qt.DockWidgetArea(2) #2 # right side by default
        self.isVisible = True
        self.isFloating = False
        self.floatingPosX = 0
        self.floatingPosY = 0
        self.width = gDefaultTagSelectorSizeArea
        self.height = gDefaultTagSelectorSizeAreaHeight

    def toString(self) -> str:
        return "visible: " + str(self.isVisible) + \
                "   isFloating: " + str(self.isFloating)+ \
                "   position: " + str(self.position)

    def __repr__(self) -> str:
        return self.toString()