
from .widgets.tagselectorgui import TagSelectorGui
from .ankihelper.guidialoginjector import GuiDialogInjector
from .datapersister.tsdatapersister import TSDataPersistent
from .ankihelper.noteeditorwrapper import NoteEditorWrapper


def getTagSelector(dialog):
    if(hasattr(dialog,"tagSelector")):
        return dialog.tagSelector
    return None


def setDialogTagSelector(dialog, ts):
    dialog.tagSelector = ts


class TagSelector:
    """
        This class is the base node for everything. It holds members for
        the gui-structure and data-structure

        Notice@attaching this class to Anki mw
            We cannot save this class inside the mw, because wa have gui
            attached to it. And the user can open AddCards and Browser
            simultaniously. So we would have broken GUI links
    """

    def __init__(self, ankiconfig):
        """ addCardsDialogForm = whole AddCards-dialog
        aqtEditorObjet = contained object within the AddCards-dialog, that contains
                        things like the fields for Data-input"""
        self._tagSelectorData =  TSDataPersistent()
        self._ankiconfig = ankiconfig
        self._minCountOfTagSelectorItems = ankiconfig["default number of tag fields"]
        self.tsItemsArray = []
        pass



    def setData(self, tsDataPersistend):
        self._tagSelectorData = tsDataPersistend

    def getData(self):
        return self._tagSelectorData

    def dugGetDataArrayAsString(self) -> str:
        """return: sring of the items array"""
        return self.getData().getItemsAsString()


    def createStaticGui(self, addCardsOrBrowserDialog):
        addDialogForm = addCardsOrBrowserDialog.form
        noteEditor = NoteEditorWrapper(addCardsOrBrowserDialog.editor)

        # this will setup our gui we can operate on
        self._gui = TagSelectorGui(addDialogForm,
                                   noteEditor
                                ,self._ankiconfig["Column headline"]
                                #TagSelector._minCountOfTagSelectorItems,
                                #1,
                                ,self._ankiconfig["Default width for TagSelector"]

                                )

        # todo: move it to a better place
        #showInfo("dug: before injectDockingWidget; \n floating: " + str(self.getData().dockWidgetData.isFloating))
        GuiDialogInjector.injectDockingWidget(
                                self._ankiconfig
                                , addDialogForm
                                , addCardsOrBrowserDialog
                                , self._gui
                                , self.getData().dockWidgetData)

        # included into __init__ of TSGui
        #guiVLayout = self._gui.createStaticGui(qDockWidgetContent)
        #addDialogForm._fieldsAreaHLayout.addLayout(guiVLayout)
        pass


    def updateDataFromGui(self):
        # must ONLY forward! Dockwidget is not part of TS! So it must not be saved here!
        self.setData(self._gui.updateTSDataFromTSGui(self.getData()))

    def updateGuiFromData(self):
        # just a forwarder function
        return self._gui.updateTSGuiFromTSData(self.getData(), self._minCountOfTagSelectorItems)


    def _insertData(self, savedTagSelector):
        #showInfo("TagSelector._insertData() was called")
        # check: do we have enough items on our gui?

        guiItemCountToAdd = len(self.tsItemsArray) - len(savedTagSelector._tagSelectorItems)

        try:
            i = 0
            for tsItem in savedTagSelector._tagSelectorItems:
                self.tsItemsArray[i].setTagsString(tsItem)
                i = i + 1
        except:
            pass # just ignore errors in case of uncongruency between gui and data

