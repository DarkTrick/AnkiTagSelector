
from ..widgets.tsmainwindow import TSMainWindow
from ..datamodel.dockwidgetdata import DockWidgetData
from ..tsutils.glogger import gLogger
from ..widgets.tsdockwidgetgui import TSDockWidget
from ..ankihelper.noteeditdialogwrapper import NoteEditDialogWrapper

class GuiDialogInjector:

    # --------------------------------------------------------------------------

    @staticmethod
    def getAddonMainWindow(dialogForm, dialog: NoteEditDialogWrapper):
        """ return the addonMainWindow (that can be used from foreign classes
            as well. It will only be created, if necessary. Otherwise just
            returned"""
        if(hasattr(dialogForm, "addonMainWindow") == False):
            mainWindow = TSMainWindow(dialog)
            # move the current anki-content inside a main-window.
            mainWindow.setCentralWidget(dialogForm.fieldsArea)
            dialogForm.addonMainWindow = mainWindow
        return dialogForm.addonMainWindow

    @staticmethod
    def injectDockingWidget(
             ankiconfig: dict
            ,addCardsDialogForm
            ,dialog: NoteEditDialogWrapper
            ,dockWidgetContentSizable
            ,dockWidgetData = DockWidgetData()):
        """@return: Widget for the/a new area"""

        gLogger.debug("__init__::GuiDialogInjector::injectDockingWidgetCalled")
        # ----------------------------------------------------------------------
        # ---------- create main window ----------------------------------------
        # ----------------------------------------------------------------------
        mainWindow = GuiDialogInjector.getAddonMainWindow(addCardsDialogForm, dialog)

        """
            The Input-fields at the addcards-dialog (addCardsDialogForm.fieldsArea)
                originally lives inside the 2nd row of addCardsDialogForm.verticalLayout.
        """

        # If we're working inside the editCurrent dialog, we need a different
        #   postion to inject our mainwindow in. Otherwise the Close-Button
        #   will go on top of the dialog
        posToInsert = 1
        if(dialog.isEditCurrentDialog()):
            posToInsert = 0

        # get the widget to insert the tagselector into
        tagSelectorAnchor = None
        try:
            # anki 24.06.03
            tagSelectorAnchor =  addCardsDialogForm.verticalLayout_3
        except:
            # older anki versions
            tagSelectorAnchor =  addCardsDialogForm.verticalLayout



        tagSelectorAnchor.insertWidget(posToInsert,mainWindow)


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
        tsDockWidget.setWindowTitle(ankiconfig["Title"])


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
        dialog.setCurrentDockWidget(tsDockWidget)
        addCardsDialogForm.tsDockWidgetContents = dockWidgetContentSizable


    # --------------------------------------------------------------------------


    @staticmethod
    def getCurrentDockWidgetData(dialog: NoteEditDialogWrapper):
        """ This method return the DockWidgetData (only the data), that is sitting
            inside the DockWidged. The DockWidget is inside the "addCardsWidget"
            object. This class creates and enchains the Dockwidget, so it handles
            all calls to it.
        """
        # why is this function here?
        #   this function is in this class, because the dockWidget will be created here

        addCardsDialogForm = dialog.getForm()
        dockData = DockWidgetData()

        dockWidget = dialog.getCurrentDockWidget()
        dockWidgetArea = addCardsDialogForm.addonMainWindow.dockWidgetArea(dockWidget)

        dockData.position = dockWidgetArea
        # why "isVisible**to**"?: when this function is called, the dialog is already closed
        #   so it will always not be visible. Therefore we check the state in relation
        #   to the window it's sitting in
        dockData.isVisible = dockWidget.isVisibleTo(dialog.getWidget())
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
