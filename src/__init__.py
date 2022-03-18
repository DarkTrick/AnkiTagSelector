from .easyconfig import *
#############################################################
#                                                           #
#                      CONFIGURATION                        #
#                                                           #
#############################################################

# enable/disable TagSelector
gEnableTagSelectorInAddCards = YES
gEnableTagSelectorInBrowser = NO # does not work anymore after Anki 2.1.46
gEnableTagSelectorInEditNotes = YES

gShareDataAmongDecks = NO # if this is said to "YES", you can access the same tags
                          #   from all decks

# set string in titlebar:
gTitleBarString = "Tag Selector"
#gTitleBarString = "        Tags"

# set column headline for Tag selector
gColumnHeadlineString = "       Tags" # empty for no column headline

# set the distance between each tags field:
# open file "addons/tagselectorcommons/allclasses.py" and change the
#                       value gDEFAULT_SPACE_BETWEEN_TAG_FIELDS
#
#                                              sorry for the inconvenience here


# ---- unimportant settings ----

# For changing the number of Input fields, change this value:
defaultNumberOfInputFields = 1

# changing default size of TagSelectorArea
gDefaultTagSelectorSizeArea = 170


# for making data avaiable all over anki without HDD read/write
# And enablign config-Feature
from aqt import mw
# Enable config in Anki2.1
config = mw.addonManager.getConfig(__name__)



"""     Notice for Users  ''''

    - Data is only saved to disk (permanently), when Anki is closed. If Anki
        crashes, changes are lost. This is in favour to SSD users

"""




"""     Notice for Developers:  '''''

        - This addon uses the addonMainWindow inside a dialog.
        ( it will be created if not present and used if present )

        - TagSelector will always be glued to Browser(QDialog).tagSelector
                                          or AddCards(QDialog).tagSelector
        - TagSelectorData will always be glued to mw.tagSelectorData
"""

##############################################################
### Code starts from here:


#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------

# this will be the entry name under Tools->Add-Ons
gNAME_OF_THIS_FILE = 'TagSelector'
gAddonNamePrettyString = "Tag Selector"

# ==============================================================================
""" reason for this? Don't spread "mw.tagSelectorData" calls all over the code
    with the need to change, if we make a change. Or even worse: spread typos"""
gITEM_NAME_OF_OBJECT_IN_ANKI_MW = "tagSelectorData"
gITEM_NAME_OF_OBJECT_IN_DIALOG = "tagSelector"
def getTsDataFromAnkiMw():
    if(hasattr(mw,"tagSelectorData")):
        return mw.tagSelectorData
    return None

def isAnkiDataInMwAvailable():
    if(hasattr(mw,gITEM_NAME_OF_OBJECT_IN_ANKI_MW)):
        if(not (None == getTsDataFromAnkiMw())):
            return True
    return False

def setTsDataInAnkiMw(tsData):
    mw.tagSelectorData = tsData

def getTagSelector(dialog):
    if(hasattr(dialog,"tagSelector")):
        return dialog.tagSelector
    return None


def setDialogTagSelector(dialog, ts):
    dialog.tagSelector = ts

# ==============================================================================

from anki.hooks import addHook
from anki.hooks import wrap

# for injection in these dialogs
from aqt.editor import Editor
from aqt.browser import Browser
from aqt.editcurrent import EditCurrent
from aqt.qt import qconnect

from aqt.utils import showInfo

from aqt.addcards import AddCards
from PyQt5 import QtCore, QtGui # Core for Signals; Gui for gui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMainWindow

# for saving data:
import pickle # write to fs
import os # handling paths

# TagSelector classes (self implemented)
from .tagselectorgui import *
from .allclasses import *

# for making a resizable docking-area
from .QtAdditions import WidgetSizeable


# ========================================================================
# ========================================================================
"""
        IMPORTANT NOTE FOR STRING-MANIPULATION

        It is not allowed to use the "str"-Function for userdata in any way!
        Why? because it can't handle non-ASCII-characters!

        Use unicode(aString,"utf-8") instead
"""


"""
Structure:

  __________________________
 |                          |
 |     TSDataPersistent      |
 |__________________________|
 |                          |~~~~~~ contains all data, that is going to
 |    TagSelectorItem       |       be made persistent.
 |    TagSelectorItem       |
 |    TagSelectorItem       |
 |          .               |
 |          .               |
 |          .               |
 |__________________________|
             ^
             |
             |
  ___________|_______
 |                   |
 |   TagSelector     |
 |___________________|~~~~~ This is basically the program. All gui-stuff
 |                   |      and so on goes here. This object will not be
 |                   |      saved. But it can save it's *data* through
 |  TSDataPersistent  |      TSDataPersistent.
 |                   |
 |___________________|

"""


# ========================================================================
# ========================================================================

class SessionPersistenceMgmt:

        @staticmethod
        def loadDataFromMwOrFs():
            """
            @return: a functional tsDataObject (guaranteed)

            will NOT update gui data after loading!
            returns a TagSelector-Object

            1. check: do we have a TS inside the mw
            2.1 yes: just use it
            2.1 no: try to load from file or create new one"""
            #showInfo("loadDataFromMwOrFs")
            tsDataNew = None
            gLogger.debug("__init__::loadDataFromMwOrFs")
            # === first: try to load from mw (anki-god)===
            if( isAnkiDataInMwAvailable()):
                # make TS persistent for next call
                tsDataNew = getTsDataFromAnkiMw()
                gLogger.debug("__init__::data from Mw loaded")
                #showInfo("dug: get data from mw; \nfloating: " + str(tsDataNew.dockWidgetData.isFloating))
            else: # === second: try to load from file ===
                tsDataNew = TSDataPersistent.PersistanceMgmt.loadDataFromFilesystem()
                #showInfo("dug: get data from file")
                gLogger.debug("__init__::load from fs")
                # === third: no mw-data, no saved files => just use empty data === #
                if(None == tsDataNew):
                    tsDataNew = TSDataPersistent()
                    gLogger.debug("__init__::   nothing found; use a new one")
                    pass

                # now save it in Mw for the next time
                setTsDataInAnkiMw(tsDataNew)

            return tsDataNew


        # --------------------------------------------------------------------
        @staticmethod
        def updateAnkiMwTSGuiLayoutFromDialog(addCardsOrBrowserDialog):
            """This method persists only the dialog data (e.g. size,
                position, visibility etc) inside the AnkiMw-Object"""
            pass

        @staticmethod
        def updateAnkiMwTSContentDataFromDialog(addCardsOrBrowserDialog):
            """This method persists only the content data of the TS
                ( e.g. Number of tags, content of tag fields, ...)"""

            # ATTENTION FOR CHANGES:
            """this is a copy&paste-part from the function
            updateAnkiMwDataFromGui. We could clean up, but as always...
            I'm afraid of breaking something and I want to get it done.
            So take care, if you ever change this part"""
            gLogger.debug("__init__::updateAnkiMwTSContentDataFromDialog called")

            if(hasattr(addCardsOrBrowserDialog,gITEM_NAME_OF_OBJECT_IN_DIALOG)):
                gLogger.debug("__init__::     save TS data to mw")
                ts = getTagSelector(addCardsOrBrowserDialog)
                ts.updateDataFromGui()
            else:
                gLogger.debug("__init__::     no tagSelector found, that we could save")

        # --------------------------------------------------------------------

        @staticmethod
        def updateAnkiMwDataFromGui(addCardsOrBrowserDialog):
            gLogger.debug("__init__::updateAnkiMwDataFromGui called")

            if(hasattr(addCardsOrBrowserDialog,gITEM_NAME_OF_OBJECT_IN_DIALOG)):
                # ATTENTION FOR CHANGES:
                """this is a copy&paste-part from the function
                updateAnkiMwTSContentDataFromDialog. We could clean up, but as always...
                I'm afraid of breaking something and I want to get it done.
                So take care, if you ever change this part"""
                gLogger.debug("__init__::     save TS data to mw")
                ts = getTagSelector(addCardsOrBrowserDialog)
                ts.updateDataFromGui()
                # now try and save the state of our gui to mw(anki-god)
                try:
                    gLogger.debug("__init__::     save DockWidget data to mw")
                    dockData = GuiDialogInjector.getCurrentDockWidgetData(
                                addCardsOrBrowserDialog)
                    gLogger.debug("__init__::     " + dockData.toString())
                    ts.getData().setDockWidgetData( dockData )
                    getTsDataFromAnkiMw().setDockWidgetData( dockData )
                except:
                    gLogger.debug("__init__::     could not save DockWidget data to mw")
                    pass # couldn't save data. That probably happened, because
                    # the browser was opened and closed, without opening a card even once
                    #showInfo("dug: couldn't save widget data")
            else:
                pass
                gLogger.debug("__init__::     no tagSelector found, that we could save")
                #showInfo("dug: no tagSelector found, that we could save")
            pass

    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

# --------------------------------------------------------------------
# --------------------------------------------------------------------

class TagSelector:
    """
        This class is the base node for everything. It holds members for
        the gui-structure and data-structure

        Notice@attaching this class to Anki mw
            We cannot save this class inside the mw, because wa have gui
            attached to it. And the user can open AddCards and Browser
            simultaniously. So we would have broken GUI links
    """
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

    # ==================  static variables  ==============================
    minCountOfTagSelectorItems = config["default number of tag fields"]

    # -------------------------------------------------------------------

    def __init__(self):
        """ addCardsDialogForm = whole AddCards-dialog
        aqtEditorObjet = contained object within the AddCards-dialog, that contains
                        things like the fields for Data-input"""
        self._tagSelectorData =  TSDataPersistent()
        pass

    # -------------------------------------------------------------------


    def setData(self, tsDataPersistend):
        self._tagSelectorData = tsDataPersistend

    def getData(self):
        return self._tagSelectorData

    def dugGetDataArrayAsString(self):
        """return: sring of the items array"""
        return self.getData().getItemsAsString()

    # -------------------------------------------------------------------

    def createStaticGui(self, addCardsOrBrowserDialog):
        addDialogForm = addCardsOrBrowserDialog.form
        objectForGuiInjection = addCardsOrBrowserDialog.editor


        # this will setup our gui we can operate on
        self._gui = TagSelectorGui(addDialogForm,objectForGuiInjection
                                ,config["Column headline"]
                                #TagSelector.minCountOfTagSelectorItems,
                                #1,
                                ,config["Default width for TagSelector"]

                                )

        # todo: move it to a better place
        #showInfo("dug: before injectDockingWidget; \n floating: " + str(self.getData().dockWidgetData.isFloating))
        GuiDialogInjector.injectDockingWidget( \
                                addDialogForm
                                ,addCardsOrBrowserDialog
                                , self._gui
                                , self.getData().dockWidgetData)

        # included into __init__ of TSGui
        #guiVLayout = self._gui.createStaticGui(qDockWidgetContent)
        #addDialogForm._fieldsAreaHLayout.addLayout(guiVLayout)
        pass

    # -------------------------------------------------------------------

    def updateDataFromGui(self):
        # must ONLY forward! Dockwidget is not part of TS! So it must not be saved here!
        self.setData(self._gui.updateTSDataFromTSGui(self.getData()))

    def updateGuiFromData(self):
        # just a forwarder function
        return self._gui.updateTSGuiFromTSData(self.getData(), TagSelector.minCountOfTagSelectorItems)

    # -------------------------------------------------------------------

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

    # -------------------------------------------------------------------

# ========================================================================
# ========================================================================

class TSMainWindow(QMainWindow):
    """Special main window, that forwards a close event
    to a containing dialog
    Reason for this class:
     - "Esc" in addCardsDialog would destroy the mainwindow
        (that is needed for the dockwidget), but not the dialog.
        The result is an almost empty addCards dialog. To prevent
        this, we need to forward close events from this mainwindow
        to the surrounding dialog"""

    def __init__(self, surroundingDialog):
        """@param surroundingDialog: should be an addCards dialog (or similar)"""
        super(TSMainWindow, self).__init__()
        self.parentDialog = surroundingDialog

    def closeEvent(self, closeEvent):
        gLogger.debug("TSMainWindow::closeEvent")
        closeEvent.ignore()
        try:
            self.parentDialog.reject()
        except:
            gLogger.debug("TSMainWindow::closeEvent: reject didnt work")
            # once, this happend in the browser.
            # no idea how and why that happened...
            # just try close() randomly
            try:
                self.parentDialog.close()
                gLogger.debug("TSMainWindow::closeEvent: close worked")
            except:
                pass

# ========================================================================
# ========================================================================

class GuiDialogInjector:

    # --------------------------------------------------------------------------

    @staticmethod
    def getAddonMainWindow(dialogForm, addCardsDialog):
        """ return the addonMainWindow (that can be used from foreign classes
            as well. It will only be created, if necessary. Otherwise just
            returned"""
        if(hasattr(dialogForm, "addonMainWindow") == False):
            mainWindow = TSMainWindow(addCardsDialog)
            # move the current anki-content inside a main-window.
            mainWindow.setCentralWidget(dialogForm.fieldsArea)
            dialogForm.addonMainWindow = mainWindow
        return dialogForm.addonMainWindow

    @staticmethod
    def injectDockingWidget(addCardsDialogForm
            ,addCardsDialog
            ,dockWidgetContentSizable
            ,dockWidgetData = DockWidgetData()):
        """@return: Widget for the/a new area"""

        gLogger.debug("__init__::GuiDialogInjector::injectDockingWidgetCalled")
        # ----------------------------------------------------------------------
        # ---------- create main window ----------------------------------------
        # ----------------------------------------------------------------------
        mainWindow = GuiDialogInjector.getAddonMainWindow(addCardsDialogForm, addCardsDialog)

        """
            The Input-fields at the addcards-dialog (addCardsDialogForm.fieldsArea)
                originally lives inside the 2nd row of addCardsDialogForm.verticalLayout.
        """

        # If we're working inside the editCurrent dialog, we need a different
        #   postion to inject our mainwindow in. Otherwise the Close-Button
        #   will go on top of the dialog

        posToInsert = 1
        if(type(addCardsDialog).__name__ == "EditCurrent"):
            posToInsert = 0

        addCardsDialogForm.verticalLayout.insertWidget(posToInsert,mainWindow)

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!! TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:TODO:
        # !!!!!!! The dockWidget should actually be created inside the TagSelectorGui!!!!
        # !!!!!!! we should only pass the mainwindow into it
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!
        # ----------------------------------------------------------------------
        # --------- create tsDockWidget to put the TagSelector in --------------
        # ----------------------------------------------------------------------

        tsDockWidget = TSDockWidget(mainWindow)
        tsDockWidget.specialInit()
        tsDockWidget.setObjectName("tsDockWidget2")
        tsDockWidget.setWindowTitle(config["Title"])


        # ----------------------------------------------------------------------
        # ----------- Create Widget, where the dockwidget is contained ---------
        # ----------------------------------------------------------------------

        # TODO: use the code below and see, if we get the scrolling feature.
        #       Be careful! This might interfere with the resizing, because
        #       restoring size uses widget()
        #scrollArea = QScrollArea(tsDockWidget)
        #tsDockWidget.setWidget(scrollArea)
        #scrollArea.setWidget(dockWidgetContentSizable)

        tsDockWidget.setWidget(dockWidgetContentSizable)


        # ----------------------------------------------------------------------
        # ----------------- configure our widget -------------------------------
        # ----------------------------------------------------------------------
        # use the config-data we received through parameter for the creation
        mainWindow.addDockWidget(dockWidgetData.position, tsDockWidget)

        # the resizing must be called before show is called! due to the lack of qt
        #   to actually resize a widget programmatically
        dockWidgetContentSizable.resize(dockWidgetData.width, dockWidgetData.height)

        if(dockWidgetData.isVisible == False):
            tsDockWidget.hide()
        # ATTENTION: tsDockWidget.show() must not be called here!
        #   we will wait, until it is called automatically.
        #   because we can't resize our window after the call!
        #else:
            #tsDockWidget.show()

        # must be after resize. therwise we don't have correct resizing (e.g. wrong height)
        if(dockWidgetData.isFloating == True):
            tsDockWidget.setFloating(dockWidgetData.isFloating)
            tsDockWidget.move(dockWidgetData.floatingPosX,dockWidgetData.floatingPosY)

        # ----------------------------------------------------------------------
        # ---------------- add everything to anki object -----------------------
        # ----------------------------------------------------------------------
        GuiDialogInjector.setCurrentDockWidget(addCardsDialog,tsDockWidget)
        addCardsDialogForm.tsDockWidgetContents = dockWidgetContentSizable


    # --------------------------------------------------------------------------

    @staticmethod
    def getCurrentDockWidget(dialog):
        return dialog.form.tsDockWidget

    @staticmethod
    def setCurrentDockWidget(dialog, dockwidget):
        dialog.form.tsDockWidget = dockwidget

    @staticmethod
    def getCurrentDockWidgetData(addCardsWidget):
        """ This method return the DockWidgetData (only the data), that is sitting
            inside the DockWidged. The DockWidget is inside the "addCardsWidget"
            object. This class creates and enchains the Dockwidget, so it handles
            all calls to it.
        """
        # why is this function here?
        #   this function is in this class, because the dockWidget will be created here

        addCardsDialogForm = addCardsWidget.form
        dockData = DockWidgetData()

        dockWidget = GuiDialogInjector.getCurrentDockWidget(addCardsWidget)
        dockWidgetArea = addCardsDialogForm.addonMainWindow.dockWidgetArea(dockWidget)

        dockData.position = dockWidgetArea
        # why "isVisible**to**"?: when this function is called, the dialog is already closed
        #   so it will always not be visible. Therefore we check the state in relation
        #   to the window it's sitting in
        dockData.isVisible = dockWidget.isVisibleTo(addCardsWidget)
        dockData.isFloating = dockWidget.isFloating()
        dockData.floatingPosX = dockWidget.pos().x() #20 # TODO: put a real value here
        dockData.floatingPosY = dockWidget.pos().y() #20 # TODO: put a real value here
        dockData.width = dockWidget.widget().width()
        dockData.height = dockWidget.widget().height()

        return dockData

    # --------------------------------------------------------------------------

    @staticmethod
    def removeDockWindow(FormObject):
        gLogger.debug("__init__::GuiDialogInjector::removeDockWindow()")
        FormObject.addonMainWindow.removeDockWidget(FormObject.tsDockWidget)
        pass

    # --------------------------------------------------------------------------

    @staticmethod
    def getTagSelectorContainerWidget(FormObject):
        return FormObject.tsDockWidget

# ========================================================================
# ========================================================================


# ============================================================================================================
# ===================================                  =======================================================
# =================================   PUBLIC FUNCTIONS   =====================================================
# ===================================                  =======================================================
# ============================================================================================================

# ========================================================================

def main_TSInjection(addCardsOrBrowserDialog):
    gLogger.debug("__init__::main_TSInjection called")
    if(True or not hasattr(addCardsOrBrowserDialog,gITEM_NAME_OF_OBJECT_IN_DIALOG)):
        gLogger.debug("__init__::   - create Tag selector")
        # ---- loadTS data -----
        tagSelector = TagSelector()
        tagSelector.setData(SessionPersistenceMgmt.loadDataFromMwOrFs())
        # make our object persistent inside the dialog
        setDialogTagSelector(addCardsOrBrowserDialog, tagSelector)

        # create static gui
        tagSelector.createStaticGui(addCardsOrBrowserDialog)

        #tagSelector.createDataDependendGui()
        tagSelector.updateGuiFromData()

    pass


# ========================================================================

def main_onAddCardsDialogWasNotClosed(aqtAddCardsDialog):
    """ if the user said "no" to "are you sure to close the dialog?"
    we need this function to recreate the TS again"""
    gLogger.debug("__init__::main_onAddCardsDialogWasClosed")
    if(aqtAddCardsDialog.isVisible()):
        aqtAddCardsDialog.form.tsDockWidget.show()
    pass

def main_onMaybeCloseAddCardsDialog(addCardsOrBrowserDialog):
    """
        This function must be called BEFORE the user decides
        "if the dialog should really close".
        Save data and
    """
    gLogger.debug("__init__::main_onMaybeCloseAddCardsDialog()")
    SessionPersistenceMgmt.updateAnkiMwDataFromGui(addCardsOrBrowserDialog)
    closeTS(addCardsOrBrowserDialog)

# ========================================================================

def main_onBrowserDialogClose(browser,qCloseEvent):
    #showInfo("close browser")
    # We MUST NOT save the DockWidget-State here, as it might be hidden
    #    and would therefore lead to wrong (visibility) values.
    #    It might be hidden because the user selected several cards and
    #    then closed the browser
    SessionPersistenceMgmt.updateAnkiMwTSContentDataFromDialog(browser)
    try: #in case no note was opened inside the browser, this will fail
        closeTS(browser)
    except:
        pass


# ========================================================================

def addShowDialogMenuItemInContextMenu(AddCards_Editor_EditorWebview,menu):
    # why "try"?
    #  We can't set the hook up only for addCards / BrowerEditor. So in case
    #   we can't access the elements (as they might have never been created)
    #   just ignore that
    try:
        # The only parameter we can get passed is the WebView. So we have to climb up the
        #   parents-ladder.
        tsDockWidget = AddCards_Editor_EditorWebview.editor.parentWindow.form.tsDockWidget
        a = menu.addAction(_("show " + gAddonNamePrettyString))

        # This function is directly implemented here, as we create the docking window here.
        a.triggered.connect(lambda showDock: tsDockWidget.show())

        # only enable the menu item, if it's necessary
        if(tsDockWidget.isVisible()):
            a.setEnabled(False)
    except:
        pass

    pass


# ========================================================================

def getAlreadyDestroyed(dialog):
    if(hasattr(dialog,"alreadyDestroyed")):
        alreadyDestroyed = dialog.alreadyDestroyed
    else:
        alreadyDestroyed = True
    return alreadyDestroyed




def main_onBrowserItemChangedAfter(browserDialog, currentNote, previousNote):
    """After a new card was selected, - if it's a single one - insert TagSelector"""
    gLogger.debug("__init__::start TS from BrowseritemChanged")
    alreadyDestroyed = getAlreadyDestroyed(browserDialog)

    if(hasattr(browserDialog,"singleCard")):
        if(browserDialog.singleCard is True and alreadyDestroyed is True):
            #showInfo("SingleCard is True")
            main_TSInjection(browserDialog)
            browserDialog.alreadyDestroyed = False
        pass


# ==============================================================================

def closeTS(addCardsOrBrowserObject):
    # make sure the window hides, if it is undocked, when form is closed
    addCardsOrBrowserObject.form.tsDockWidget.close()


# ========================================================================


def test2(obj):
    showInfo("test2 called")

    pass

# ========================================================================

def clearData():
    # remove file data
    TSDataPersistent.PersistanceMgmt.clearData()
    # clean the current data
    if(hasattr(mw, gITEM_NAME_OF_OBJECT_IN_ANKI_MW)):
        setTsDataInAnkiMw(TSDataPersistent())
    pass

def deactivate_notReally():
    # hard to implement, so we just tell the user, how to get this feature
    showInfo("For deactivation, please follow the following steps:"
            "\n1. Open AddOn-Menu -> " + gNAME_OF_THIS_FILE + " -> 'Edit...'"
            "\n2. Set 'gEnableTagSelector' to 'NO'"
            "\n3. restart Anki" )

def main_unloadTagSelector():
    gLogger.debug("__init__::Unload Tag Selector")
    """save data to disk, remove object from mw"""

    # Save to file do Disk only when anki is closed ( don't stress SSDs )
    #   we must hook "before" to be able to get our data (otherwise it's already
    #   destroyed)

    if(isAnkiDataInMwAvailable()):
        TSDataPersistent.PersistanceMgmt.saveDataToFilesystem(getTsDataFromAnkiMw())
    # set it back to None to show, it's not present anymore
    setTsDataInAnkiMw(None)
    gLogger.debug("__init__::    tsData:" + str(mw.tagSelectorData))



gSetupTagSelectorFinished = False
def main_onProfileLoad():
        gLogger.debug("__init__::onProfileLoad")
        """ This function is here, so addons are loaded *AFTER* the profile was chosen"""
        # ==========================================================================
        # ============= first things to do: set global variables!   ================
        # ==========================================================================
        tmpDir = os.path.join(mw.col.media.dir(),"..")
        if(config["Share tag data among decks"] == "YES"): # if we share, put it inside the head folder, so go one level up:
            tmpDir = os.path.join(tmpDir,"..")
        TSDataPersistent.PersistanceMgmt.static_PathToConfigFile = tmpDir


        global gSetupTagSelectorFinished
        if(not gSetupTagSelectorFinished):
            gLogger.debug("__init__::    do only once-stuff")
            gSetupTagSelectorFinished = True
            # ==========================================================================
            # ============= create menu items under Addons: ===================
            # ==========================================================================
            mw.TS_actionClearData = QAction("clear saved data", mw)
            mw.TS_actionClearData.triggered.connect(clearData)

            # create tagselector specific menu item
            tsMenu = QMenu(gAddonNamePrettyString, mw)
            a = tsMenu.addAction("clear saved data")
            qconnect(a.triggered, clearData)


            # insert it into GUI
            try:
                # note: 'try' because we don't want to crash if
                #       anki internals for menues changed
                menu = mw.form.menuTools
                menu.insertMenu(mw.form.actionAdd_ons, tsMenu)
            except:
                pass

            #mw.form.menuExtras
            # The menu goes to
            # Tools -> Add-Ons -> TagSelector
# Code for old anki
##            for child in mw.form.menuPlugins.children():
##                try:
##                    if(child.title() == gNAME_OF_THIS_FILE):
##                        child.addAction(TS_actionClearData)
##                        child.addAction(TS_actionDeactivate)
##                        break
##                except:
##                    continue

def main_wrapFunctions():
    gLogger.debug("__init__::wrapFunctions")
    # ==========================================================================
    # ==========================================================================
    # ===============  set all the hooks & wraps for TS ========================
    # ==========================================================================
    # ==========================================================================
    if (config["Enable TagSelector in AddCards"] == "YES"):
        AddCards.setupEditor = wrap(AddCards.setupEditor, main_TSInjection)
        # problem with reject is: our method is called, even if the user pressed "no"
        #   , because everything happens in the same method (see addcars.reject)
        try:
            # newer Ankiverions:
            AddCards._reject = wrap(AddCards._reject, main_onMaybeCloseAddCardsDialog,"before")

        except:
            gLogger.debug("main_wrapFunctions()::fallback version of wraps")
            # fallback for older ankiversions
            AddCards.reject = wrap(AddCards.reject, main_onMaybeCloseAddCardsDialog,"before")
            AddCards.reject = wrap(AddCards.reject, main_onAddCardsDialogWasNotClosed)


    #if (config["Enable TagSelector in Browser"] == "YES"):
    #    Browser.onRowChanged = wrap(Browser._onRowChanged, main_onBrowserItemChangedAfter)
    #    Browser.closeEvent = wrap(Browser.closeEvent, main_onBrowserDialogClose, "before")
    #    #Browser.closeEvent = wrap(Browser.closeEvent, test, "before")

    if(config["Enable TagSelector in EditNotes"] == "YES"):
        def bufferForInjection(diag, unused):
            gLogger.debug("__init__::start TS from EditCurrentDialog")
            main_TSInjection(diag)
            pass
        EditCurrent.__init__ = wrap(EditCurrent.__init__, bufferForInjection)
        EditCurrent.reject = wrap(EditCurrent.reject, main_onMaybeCloseAddCardsDialog)
        pass

    addHook("EditorWebView.contextMenuEvent",addShowDialogMenuItemInContextMenu)




# reduce overall-overhead, if nothing is enabled


if( config["Enable TagSelector in AddCards"] == "YES"
or config["Enable TagSelector in Browser"] == "YES"
or config["Enable TagSelector in EditNotes"] == "YES"):
#if(True or gEnableTagSelectorInAddCards or gEnableTagSelectorInBrowser or gEnableTagSelectorInEditNotes):
    addHook("profileLoaded", main_onProfileLoad)
    main_wrapFunctions()
    addHook("unloadProfile", main_unloadTagSelector)



# ============================================================================================================
# ============================================================================================================
# ============================================================================================================