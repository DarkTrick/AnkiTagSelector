#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------

from ..qthelper.qtimports import QtCore, QtGui
from ..qthelper.qtimports import QWidget

class WidgetSizeable(QWidget):
    #_sizehint = None

    def __init__(self, parent = None):
        #self._sizehint = None
        self._sizehint = QtCore.QSize(1, 1)
        super(WidgetSizeable,self).__init__(parent)



    def resize(self, width, height):
        ##self._sizehint = QtCore.QSize(width, height)
        # just change values, so the object stays the same!

        super(WidgetSizeable,self).resize(width, height)
        self._sizehint.setWidth(width)
        self._sizehint.setHeight(height)

    def sizeHint(self):
        if self._sizehint is not None:
            return self._sizehint
        return super(WidgetSizeable, self).sizeHint()


""" Function to recursively clear all elements inside a layout"""
def deleteItemsOfLayout(layout):
     if layout is not None:
         while layout.count():
             item = layout.takeAt(0)
             widget = item.widget()
             if widget is not None:
                 widget.setParent(None)
             else:
                 deleteItemsOfLayout(item.layout())




