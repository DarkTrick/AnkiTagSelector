#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------

"""
        ********   important! ************

        this file must be completely free from any anki-code to make it starable
        in a usual qt-application!


"""


from PyQt5 import QtCore, QtGui # Core for Signals; Gui for gui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import *

#from allclasses import TagSelectorItemBaseInterface
#from allclasses import ComprehensiveFunctions
from .allclasses import *
from .QtAdditions import *

# TODO: delete before check-in
#from aqt.utils import showInfo

"""
    A DockWidget looks as followes:

     _______________________
    |     QDockWidget       |
    |   __________________  |
    |  |    QWidget       | |
    |  |                  | |
    |  |  <here goes all  | |
    |  |    the content>  | |
    |  |__________________| |
    |                       |
    |_______________________|

    the one in the middle is the _contentWidget in here

"""

# ===============================================================
# ====== for special colors,  ===================================
# ======   remove the marked "return" below and set colors ======
# ===============================================================
BG_COLOR_TITLE_BAR = QColor(120,120,255,255)
TS_BG_COLOR = QColor(120,255,255,120)
BG_COLOR_TAGS = QColor(0,255,0,20)

def changeBGColor(widget, color = Qt.blue):
    return # remove this line to make colors work

    if(color == None):
        return
    p = widget.palette()
    p.setColor(widget.backgroundRole(), color)
    widget.setPalette(p)
    widget.setAutoFillBackground(True)

# ===============================================================



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
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
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
    


# BIG TODO: restructure:
#   The dockWidget and stuff should be created here, so we'd only a mainwindow,
#   where all of our gui goes

class TagSelectorGui(WidgetSizeable):
    """ creates guiElements that is shown in Anki"""

    # --------------------------------------------------------------------

    def __init__(self, aqtAddCardsDialog, aqtEditor #numOfItemsToCreate,
                        , columnHeadlineString
                        ,lineEditMinimumWidth = 70
                        , dockWidgetSizeWidth = 100
                        , dockWidgetSizeHeight = 100
                        , parent = None ):
        super(TagSelectorGui,self).__init__(parent)

        gLogger.debug("TagSelectorGui.__init__")

        self.lineEditMinimumWidth = lineEditMinimumWidth
        self.tsItemsArray = []
        self.dockWidgetSizeWidth = dockWidgetSizeWidth
        self.dockWidgetSizeHeight = dockWidgetSizeHeight

        # needed for giving the generated buttons access to the full editor-gui
        #   ( editor-gui = all the things for input inside the AddCards-dialog )
        self.aqtEditor = aqtEditor

        # needed for making the docked window
        self.aqtAddCardsDialog = aqtAddCardsDialog

        # here's where we put all our TagSelector items in
        self.tsItemAreaLayout = None

        self._createStaticGui(columnHeadlineString)

        self._addContextMenu()

        pass

    # --------------------------------------------------------------------

    def _createStaticGui(self, columnHeadlineString):
        """
        return the created gui-layout element """
        gLogger.debug("TagSelectorGui::_createStaticGui")
        # put elements, where we need them
        self._createTagSelectorLayout(self)

        ##self.resize(self.dockWidgetSizeWidth,self.dockWidgetSizeHeight)
        ##self.resize(100,300)
        if(not ("" == columnHeadlineString)):
            self._addColumnTitle()

        return self.tsItemAreaLayout

    # --------------------------------------------------------------------------

    def _addColumnTitle(self):
        # add label to widget ( will look like the column title)
        tagselectorExplanationLabel = QLabel()
        tagselectorExplanationLabel.setObjectName("TagselectorExplanationLabel")
        tagselectorExplanationLabel.setText("     Tags")

        self.tsItemAreaLayout.addWidget(tagselectorExplanationLabel)

    # --------------------------------------------------------------------------

    def _createTagSelectorLayout(self, parentWidget):
        # we will later put all our boxes in this created layout

        # parent Widget must directly go into the layout, so we have automatic resize
        vLayout = QVBoxLayout(self)

        # Item spacing is set to 0 => all spaces are made by the items itself
        #   therefore, we have no vLayout-space between items
        vLayout.setSpacing(0)
        # space should only be made by containing elements, so enlarge the click-area
        vLayout.setContentsMargins(0,0,0,0);

        changeBGColor(self, TS_BG_COLOR)

        vLayout.setObjectName("_TSLayout")
        #guiLayoutToInsertLayoutTo.addLayout(vLayout)

        # fine ajustments of the layout:
        vLayout.setAlignment(Qt.AlignTop)

        self.tsItemAreaLayout = vLayout

    # --------------------------------------------------------------------------

    def _addContextMenu(self):
        # connect menu call and menu open
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._openMenu)

    def _openMenu(self, position):
        # create the menu itself
        contextMenu = QMenu()
        contextMenu.addAction("add field", self.addTSItem)
        #contextMenu.addAction("remove last field", self.removeLastTSItem)

        print("menu open " + str(position))
        contextMenu.exec_(self.mapToGlobal(position))
        pass

    def addTSItem(self):
        self.addTagSelectorItems(1)

##    def removeLastTSItem(self):
##        print("remove last item")
##        itemToRemove = self.tsItemsArray.pop()
##        self.tsItemAreaLayout.removeWidget(itemToRemove.asGuiElement())
##        itemToRemove.baseElement.setParent(None)
##
##        #self.tsItemsArray.push(itemToRemove())
##        #self.removeTagSelectorItem(itemToRemove)
##        pass

    # --------------------------------------------------------------------------

    def updateTSDataFromTSGui(self, tsData):
        # Todo: improve: don't delete everything, but do changes
        srcData = self.tsItemsArray
        tsData.clearItemsData()
        destData = tsData.getItemsArray()

        for i in range(0,len(srcData)):
            tsData.addItem(TagSelectorItem(srcData[i].getTagsString()))
        pass

        return tsData

    def updateTSGuiFromTSData(self, TSData, minCountItems):
        """
            This function will create all gui Elements, that are necessary for
            the data
        """

        srcData = TSData.getItemsArray()
        destData = self.tsItemsArray

        # create necessary number of gui fields
        countOfNewGuiElementsToBeCreated = len(srcData) - len(destData)
        if(countOfNewGuiElementsToBeCreated < minCountItems):
            countOfNewGuiElementsToBeCreated = minCountItems - len(destData)

        if(countOfNewGuiElementsToBeCreated > 0):
            self.addTagSelectorItems(countOfNewGuiElementsToBeCreated)

        # fill the gui elements
        for i in range(0,len(srcData)):
            destData[i].setTagsString(srcData[i].getTagsString())


    # --------------------------------------------------------------------------

    def removeTagSelectorItem(self, tsItem):
        # find the right element and delete it
        itemToFind = tsItem.asGuiElement() # because we have HLayouts inside it and not the tsItem itself
        for i in range(self.tsItemAreaLayout.count()):
            item = self.tsItemAreaLayout.itemAt(i)
            if(item == itemToFind):
                #deleteItemsOfLayout(item.layout())
                self.tsItemAreaLayout.removeWidget(item)
                break
        itemToFind.setParent(None)
        self.tsItemsArray.remove(tsItem)

        pass

    def addTagSelectorItems(self,count):
        def _genNewPair(self, aqtEditorObject):
            """@return: return a Layout,that contains all items"""
            qtTagSelectorItem =  TSGuiItem(  \
                                    self.removeTagSelectorItem
                                    ,len(self.tsItemsArray)
                                    ,aqtEditorObject
                                    ,self.lineEditMinimumWidth
                                    ,self)
            self.tsItemsArray.append(qtTagSelectorItem)


            return qtTagSelectorItem.asGuiElement()

        if(count > 0):
            for i in range(0,count):
                #self.tsItemAreaLayout.addLayout(_genNewPair(self, self.aqtEditor))
                self.tsItemAreaLayout.addWidget(_genNewPair(self, self.aqtEditor))

    # --------------------------------------------------------------------


class MyLineEdit(QLineEdit):

    def __init__(self, removeMeCallbackFunction, parent = None):
        super(MyLineEdit,self).__init__(parent)
        self._makeCustomContextMenu()
        self.removeMeCallback = removeMeCallbackFunction
        self.textChanged.connect(self.updateTooltip)

    # --------------------------------------------------------------------------


    def _makeCustomContextMenu(self):
        # connect menu call and menu open
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._openMenu)


    def _openMenu(self, position):
        # create the menu itself
        contextMenu = self.createStandardContextMenu()
        contextMenu.addSeparator()
        contextMenu.addAction("remove item", self.removeMe)

        print("menu open " + str(position))
        contextMenu.exec_(self.mapToGlobal(position))
        pass


    def removeMe(self):
        print("remove me called")
        self.removeMeCallback(self)
        #self.addTagSelectorItems(1)

    def updateTooltip(self):
        self.setToolTip(self.text())

    # --------------------------------------------------------------------------

# ========================================================================
# ========================================================================

    # will create a new tag-selection item, that can be added to the GUI:
    #  looks like this:
    #  ____    _____________
    # |    |  |             |
    # | CB |  |  EditField  |
    # |____|  |_____________|
    #
class TSGuiItem(WidgetSizeable):
    pass
    _idOfNextElement = 0

    # --------------------------------------------------------------------------

    def setTagsString(self, stringValue ):
        self.lineEdit.setText(stringValue)

    # --------------------------------------------------------------------------

    def getTagsString(self):
        """return the tags entered as String"""
        return ComprehensiveFunctions.replaceAllWhitespaces(self.lineEdit.text()," ")

    # --------------------------------------------------------------------------

    def __init__(self, removeMeCallbackFunc, intNamePostfix, aqtEditorObject, lineEditWidth = 70
                , parent = None):
        super(TSGuiItem,self).__init__(parent) # parent is not given on purpose
        changeBGColor(self, BG_COLOR_TAGS)
        self.spaceBetweenItems = gDEFAULT_SPACE_BETWEEN_TAG_FIELDS


        self._namePostfix = "_" + str(TSGuiItem._idOfNextElement)
        TSGuiItem._idOfNextElement = TSGuiItem._idOfNextElement + 1

        self.removeMeCallbackFunc = removeMeCallbackFunc

        self.lineEditWidth = lineEditWidth

        # merge everything togerther in one layout
        # - this will be our base for using in the gui:
        self._init_createBaseElement()

        self._init_createCheckBox(self.baseElement, aqtEditorObject)
        self._init_createLineEdit(self.baseElement)

        self.mouseReleaseEvent= lambda nothing: self.checkbox.toggle()

    # --------------------------------------------------------------------------

    def _init_createBaseElement(self):
        baseWidget = self
        layout = QHBoxLayout(baseWidget)
        layout.setObjectName("hLayout" + self._namePostfix)

        # we want an appropriate space between each item. So we set the top-margin
        #   and bottom-margin to an appropriate value
        layout.setContentsMargins(10,self.spaceBetweenItems,0,self.spaceBetweenItems);

        self.baseElement = baseWidget
        self.baseLayout = layout


    # --------------------------------------------------------------------------

    def _init_createCheckBox(self, parent, aqtEditorObject):
        checkbox = QCheckBox(parent)
        self.checkbox = checkbox
        checkbox.setObjectName("checkbox" + self._namePostfix)
        self.baseLayout.addWidget(self.checkbox)

        # connect checkbox with function
        self.checkbox.toggled.connect(
            lambda checked: TSGuiItem.checkboxClicked(aqtEditorObject, checked, self) )
            #QtCore.QObject.connect(self.checkbox, QtCore.SIGNAL("toggled(bool)"),

    # --------------------------------------------------------------------------

    def removeMe(self,objToRemove):
        # remove all widgets we added
        #for i in range(self.baseElement.count()):
        #    item = self.baseElement.itemAt(i)
        #    showInfo("remove " + str(item))
        #    self.baseElement.removeItem(item)

        # call the "parent" to remove from lists
        self.removeMeCallbackFunc(self)
        pass

    # --------------------------------------------------------------------------

    def _init_createLineEdit(self, parent = None):
        lineEdit = MyLineEdit(self.removeMe) # QtGui.QLineEdit()
        self.lineEdit = lineEdit
        lineEdit.setObjectName("lineEdit" + self._namePostfix)

        #lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred);
        #lineEdit.setMinimumWidth(self.lineEditWidth)

        self.baseLayout.addWidget(self.lineEdit)

    # --------------------------------------------------------------------------

    def asGuiElement(self):
        return self.baseElement

    # --------------------------------------------------------------------------

    @staticmethod
    def checkboxClicked(EditorObject, checkboxValue, qtTagSelectorItem):
        if( checkboxValue == True):
            ComprehensiveFunctions.addTags(EditorObject,qtTagSelectorItem.getTagsString())
        else:
            ComprehensiveFunctions.removeTags(EditorObject,qtTagSelectorItem.getTagsString())
        pass

    # --------------------------------------------------------------------------
