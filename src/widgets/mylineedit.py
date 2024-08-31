#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------


from ..qthelper.qtimports import QLineEdit
from ..qthelper.qtimports import Qt_CustomContextMenu

#from allclasses import TagSelectorItemBaseInterface
#from allclasses import ComprehensiveFunctions
from ..config import *
from .QtAdditions import *

class MyLineEdit(QLineEdit):

    def __init__(self, removeMeCallbackFunction, parent = None):
        super(MyLineEdit,self).__init__(parent)
        self._makeCustomContextMenu()
        self.removeMeCallback = removeMeCallbackFunction
        self.textChanged.connect(self.updateTooltip)

    # --------------------------------------------------------------------------


    def _makeCustomContextMenu(self):
        # connect menu call and menu open
        self.setContextMenuPolicy(Qt_CustomContextMenu)
        self.customContextMenuRequested.connect(self._openMenu)


    def _openMenu(self, position):
        # create the menu itself
        contextMenu = self.createStandardContextMenu()
        contextMenu.addSeparator()
        contextMenu.addAction("remove item", self.removeMe)

        #print("menu open " + str(position))
        contextMenu.exec(self.mapToGlobal(position))
        pass


    def removeMe(self):
        #print("remove me called")
        self.removeMeCallback(self)
        #self.addTagSelectorItems(1)

    def updateTooltip(self):
        self.setToolTip(self.text())

    # --------------------------------------------------------------------------
