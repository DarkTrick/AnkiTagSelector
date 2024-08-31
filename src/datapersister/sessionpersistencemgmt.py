#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------


from .tsdatapersister import TSDataPersistent
from ..tsutils.glogger import gLogger
from ..config import *
from ..ankihelper.ankimainwindowhelper import *
from ..tagselector import getTagSelector
from ..ankihelper.guidialoginjector import GuiDialogInjector


class SessionPersistenceMgmt:

        @staticmethod
        def loadDataFromMwOrFs() -> TSDataPersistent:
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

                if(tsDataNew is not None):
                    setTsDataInAnkiMw(tsDataNew)

            if(tsDataNew is None):
                tsDataNew = TSDataPersistent()
                gLogger.debug("__init__::   nothing found; use a new one")

                # now save it in Mw for the next time
                setTsDataInAnkiMw(tsDataNew)

                return tsDataNew
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
