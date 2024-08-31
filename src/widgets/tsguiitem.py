#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------


from ..tsutils.comprehensivefunctions import ComprehensiveFunctions
from .QtAdditions import WidgetSizeable
from ..config import *
from .QtAdditions import *
from ..qthelper.qtimports import QCheckBox
from ..qthelper.qtimports import QHBoxLayout
from .mylineedit import MyLineEdit
from ..ankihelper.noteeditorwrapper import NoteEditorWrapper

class TSGuiItem(WidgetSizeable):
    """
    # will create a new tag-selection item, that can be added to the GUI:
    #  looks like this:
    #  ____    _____________
    # |    |  |             |
    # | CB |  |  EditField  |
    # |____|  |_____________|
    #
    """
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

    def __init__(self,
                 removeMeCallbackFunc,
                 intNamePostfix,
                 noteEditor: NoteEditorWrapper,
                 lineEditWidth = 70,
                 parent = None
                 ):
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

        self._init_createCheckBox(self.baseElement, noteEditor)
        self._init_createLineEdit(self.baseElement)

        self.mouseReleaseEvent= lambda nothing: self.checkbox.toggle() # type: ignore

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

    def _init_createCheckBox(self, parent, noteEditor: NoteEditorWrapper):
        checkbox = QCheckBox(parent)
        self.checkbox = checkbox
        checkbox.setObjectName("checkbox" + self._namePostfix)
        self.baseLayout.addWidget(self.checkbox)

        # connect checkbox with function
        self.checkbox.toggled.connect(
            lambda checked: TSGuiItem.checkboxClicked(noteEditor, checked, self) )
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
        lineEdit = MyLineEdit(self.removeMe)
        self.lineEdit = lineEdit
        lineEdit.setObjectName("lineEdit" + self._namePostfix)

        #Todo1: implement hook for storing data in object when editing is finished
        #   lineEdit.editingFinished.connect(custom_function)

        #lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred);
        #lineEdit.setMinimumWidth(self.lineEditWidth)

        self.baseLayout.addWidget(self.lineEdit)

    # --------------------------------------------------------------------------

    def asGuiElement(self):
        return self.baseElement

    # --------------------------------------------------------------------------

    @staticmethod
    def checkboxClicked(EditorObject: NoteEditorWrapper, checkboxValue, qtTagSelectorItem):
        if( checkboxValue == True):
            ComprehensiveFunctions.addTags(EditorObject,qtTagSelectorItem.getTagsString())
        else:
            ComprehensiveFunctions.removeTags(EditorObject,qtTagSelectorItem.getTagsString())
        pass

    # --------------------------------------------------------------------------
