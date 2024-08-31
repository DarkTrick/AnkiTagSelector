#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------


from ..qthelper.qtimports import QMainWindow
from ..tsutils.glogger import gLogger


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
