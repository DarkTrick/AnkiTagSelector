#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------

"""
        ********   important! ************

        this file must be completely free from any anki-code to make it starable
        in a usual qt-application!


"""


from ..qthelper.qtimports import QtCore
from ..qthelper.qtimports import QDockWidget
from ..qthelper.qtimports import QLineEdit
from ..qthelper.qtimports import QCheckBox
from ..qthelper.qtimports import QLabel
from ..qthelper.qtimports import QVBoxLayout
from ..qthelper.qtimports import QHBoxLayout
from ..qthelper.qtimports import QColor
from ..qthelper.qtimports import Qt
from ..qthelper.qtimports import blue
from ..qthelper.qtimports import Qt_AlignTop
from ..qthelper.qtimports import Qt_CustomContextMenu
from ..qthelper.qtimports import QMenu
from .QtAdditions import *

from ..config import *
from .tsguiitem import TSGuiItem
from ..tsutils.glogger import gLogger
from ..datamodel.tagselectoritem import TagSelectorItem
from .tsdockwidgetgui import TSDockWidget
from ..ankihelper.noteeditorwrapper import NoteEditorWrapper

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


# BIG TODO: restructure:
#   The dockWidget and stuff should be created here, so we'd only a mainwindow,
#   where all of our gui goes

class TagSelectorGui(WidgetSizeable):
    """ creates guiElements that is shown in Anki"""

    # --------------------------------------------------------------------

    def __init__(self, aqtAddCardsDialog, noteEditor: NoteEditorWrapper
                         #numOfItemsToCreate,
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
        self._noteEditor = noteEditor

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

        if (self.tsItemAreaLayout is None):
            raise Exception(f"{__name__}: self.tsItemAreaLayout is None")

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
        vLayout.setAlignment(Qt_AlignTop)

        self.tsItemAreaLayout = vLayout

    # --------------------------------------------------------------------------

    def _addContextMenu(self):
        # connect menu call and menu open
        self.setContextMenuPolicy(Qt_CustomContextMenu)
        self.customContextMenuRequested.connect(self._openMenu)

    def _openMenu(self, position):
        # create the menu itself
        contextMenu = QMenu()
        contextMenu.addAction("add field", self.addTSItem)
        #contextMenu.addAction("remove last field", self.removeLastTSItem)

        gLogger.debug("menu open " + str(position))
        contextMenu.exec(self.mapToGlobal(position))
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

        if (self.tsItemAreaLayout is None):
            gLogger.debug(f"{__name__}: self.tsItemAreaLayout is None")
            return

        # find the right element and delete it
        itemToFind = tsItem.asGuiElement() # because we have HLayouts inside it and not the tsItem itself
        for i in range(self.tsItemAreaLayout.count()):
            item = self.tsItemAreaLayout.itemAt(i)
            if(item is None):
                continue

            if(item == itemToFind):
                #deleteItemsOfLayout(item.layout())
                self.tsItemAreaLayout.removeWidget(item)
                break
        itemToFind.setParent(None)
        self.tsItemsArray.remove(tsItem)

        pass

    def addTagSelectorItems(self,count):
        def _genNewPair(self, noteEditor: NoteEditorWrapper):
            """@return: return a Layout,that contains all items"""
            qtTagSelectorItem =  TSGuiItem(  \
                                    self.removeTagSelectorItem
                                    ,len(self.tsItemsArray)
                                    ,noteEditor
                                    ,self.lineEditMinimumWidth
                                    ,self)
            self.tsItemsArray.append(qtTagSelectorItem)


            return qtTagSelectorItem.asGuiElement()

        if(count > 0):
            if(self.tsItemAreaLayout is None):
                gLogger.debug("self.tsItemAreaLayout is none")
                return

            for i in range(0,count):
                #self.tsItemAreaLayout.addLayout(_genNewPair(self, self._noteEditor))
                self.tsItemAreaLayout.addWidget(_genNewPair(self, self._noteEditor))

    # --------------------------------------------------------------------

