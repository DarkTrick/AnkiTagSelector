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


from anki.hooks import addHook # type: ignore
from anki.hooks import wrap # type: ignore

# for injection in these dialogs
from aqt.editor import Editor # type: ignore
from aqt.browser import Browser # type: ignore
from aqt.editcurrent import EditCurrent # type: ignore

from aqt.utils import showInfo # type: ignore

from aqt.addcards import AddCards # type: ignore
from aqt import mw # type: ignore

from typing import Union
from .qthelper.qtimports import QAction
from .qthelper.qtimports import QMenu

# for saving data:
import os # handling paths

# TagSelector classes (self implemented)
from .widgets.tagselectorgui import *

from .datapersister.tsdatapersister import TSDataPersistent
from .ankihelper.guidialoginjector import GuiDialogInjector
from .datapersister.sessionpersistencemgmt import SessionPersistenceMgmt
from .config import *
from .tagselector import *
from .ankihelper.ankimainwindowhelper import *
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





def main_TSInjection(ankiconfig, addCardsOrBrowserDialog):
    gLogger.debug("__init__::main_TSInjection called")
    if(True or not hasattr(addCardsOrBrowserDialog,gITEM_NAME_OF_OBJECT_IN_DIALOG)):
        gLogger.debug("__init__::   - create Tag selector")
        tagSelector = TagSelector(ankiconfig=ankiconfig)
        tagSelector.setData(SessionPersistenceMgmt.loadDataFromMwOrFs())
        # make our object persistent inside the dialog
        setDialogTagSelector(addCardsOrBrowserDialog, tagSelector)

        # create static gui
        tagSelector.createStaticGui(addCardsOrBrowserDialog)

        #tagSelector.createDataDependendGui()
        tagSelector.updateGuiFromData()

    pass



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



def getAlreadyDestroyed(dialog):
    if(hasattr(dialog,"alreadyDestroyed")):
        alreadyDestroyed = dialog.alreadyDestroyed
    else:
        alreadyDestroyed = True
    return alreadyDestroyed




def main_onBrowserItemChangedAfter(ankiconfig: dict,
                                   browserDialog,
                                   currentNote,
                                   previousNote):
    """After a new card was selected, - if it's a single one - insert TagSelector"""
    gLogger.debug("__init__::start TS from BrowseritemChanged")
    alreadyDestroyed = getAlreadyDestroyed(browserDialog)

    if(hasattr(browserDialog,"singleCard")):
        if(browserDialog.singleCard is True and alreadyDestroyed is True):
            #showInfo("SingleCard is True")
            main_TSInjection(ankiconfig, browserDialog)
            browserDialog.alreadyDestroyed = False
        pass



def closeTS(addCardsOrBrowserObject):
    # make sure the window hides, if it is undocked, when form is closed
    addCardsOrBrowserObject.form.tsDockWidget.close()


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
def main_onProfileLoad(ankiconfig: dict):
        gLogger.debug("__init__::onProfileLoad")
        """ This function is here, so addons are loaded *AFTER* the profile was chosen"""



        tmpDir = os.path.join(mw.col.media.dir(),"..")
        if(ankiconfig["Share tag data among decks"] == "YES"): # if we share, put it inside the head folder, so go one level up:
            tmpDir = os.path.join(tmpDir,"..")
        TSDataPersistent.PersistanceMgmt.static_PathToConfigFile = tmpDir


        global gSetupTagSelectorFinished
        if(not gSetupTagSelectorFinished):
            gLogger.debug("__init__::    do only once-stuff")
            gSetupTagSelectorFinished = True



            mw.TS_actionClearData = QAction("clear saved data", mw)
            mw.TS_actionClearData.triggered.connect(clearData)

            # create tagselector specific menu item
            tsMenu = QMenu(gAddonNamePrettyString, mw)
            action = tsMenu.addAction("clear saved data")
            action.triggered.connect(clearData) # type: ignore


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

def main_wrapFunctions(ankiconfig):
    gLogger.debug("__init__::wrapFunctions")





    if (ankiconfig["Enable TagSelector in AddCards"] == "YES"):
        AddCards.setupEditor = wrap(AddCards.setupEditor, lambda a: main_TSInjection(ankiconfig, a))
        # problem with reject is: our method is called, even if the user pressed "no"
        #   , because everything happens in the same method (see addcars.reject)

        # detect if the "add cards" dialog might be closed
        # Reason: <TODO>
        # try:
        #     # Anki  24.06.3
        #     pass
        # except:
        #     try:
        #         # newer Ankiverions:
        #         AddCards._reject = wrap(AddCards._reject, main_onMaybeCloseAddCardsDialog,"before")

        #     except:
        #         gLogger.debug("main_wrapFunctions()::fallback version of wraps")
        #         # fallback for older ankiversions
        #         AddCards.reject = wrap(AddCards.reject, main_onMaybeCloseAddCardsDialog,"before")
        #         AddCards.reject = wrap(AddCards.reject, main_onAddCardsDialogWasNotClosed)


    #if (config["Enable TagSelector in Browser"] == "YES"):
    #    Browser.onRowChanged = wrap(Browser._onRowChanged, main_onBrowserItemChangedAfter)
    #    Browser.closeEvent = wrap(Browser.closeEvent, main_onBrowserDialogClose, "before")
    #    #Browser.closeEvent = wrap(Browser.closeEvent, test, "before")

    # if(config["Enable TagSelector in EditNotes"] == "YES"):
    #     def bufferForInjection(diag, unused):
    #         gLogger.debug("__init__::start TS from EditCurrentDialog")
    #         main_TSInjection(diag)
    #         pass
    #     EditCurrent.__init__ = wrap(EditCurrent.__init__, bufferForInjection)
    #     EditCurrent.reject = wrap(EditCurrent.reject, main_onMaybeCloseAddCardsDialog)
    #     pass

    addHook("EditorWebView.contextMenuEvent",addShowDialogMenuItemInContextMenu)




# reduce overall-overhead, if nothing is enabled

def main(ankiconfig):
    if( ankiconfig["Enable TagSelector in AddCards"] == "YES"
    or ankiconfig["Enable TagSelector in Browser"] == "YES"
    or ankiconfig["Enable TagSelector in EditNotes"] == "YES"):
    #if(True or gEnableTagSelectorInAddCards or gEnableTagSelectorInBrowser or gEnableTagSelectorInEditNotes):
        addHook("profileLoaded", lambda: main_onProfileLoad(ankiconfig))
        main_wrapFunctions(ankiconfig)
        addHook("unloadProfile", main_unloadTagSelector)
