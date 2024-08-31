#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------


from ..qthelper.qtimports import QDockWidget, QMenu, Qt_CustomContextMenu, QtCore
from ..config import *


class TSDockWidget(QDockWidget):

    def setWidget(self, widget):
        super(TSDockWidget,self).setWidget(widget)
        _contentWidget = widget


    # --------------------------------------------------------------------------

    def specialInit(self):
        """ regardless of which QDockWidget-ctor has been used, this method
        should be called """
        self._sizehint = None
        self._contentWidget = None
        changeBGColor(self,BG_COLOR_TITLE_BAR)
        #self._addContextMenu()

    def _addContextMenu(self):
        # create the menu itself
        self.contextMenu = QMenu()
        self.contextMenu.addAction("add field", self.addTSItem)

        # connect menu call and menu open
        self.setContextMenuPolicy(Qt_CustomContextMenu)
        self.customContextMenuRequested.connect(self._openMenu)

    def _openMenu(self, position):
        print("menu open " + str(position))
        self.contextMenu.exec_(self.mapToGlobal(position))
        pass

    def addTSItem(self):
        print("add field called")

    def resize(self, width, height):
        self._sizehint = QtCore.QSize(width, height)

    def sizeHint(self):
        print('sizeHint:', self._sizehint)
        if self._sizehint is not None:
            return self._sizehint
        return super(TSDockWidget, self).sizeHint()

