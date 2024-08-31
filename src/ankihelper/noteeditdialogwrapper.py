from ..config import *
from .noteeditorwrapper import NoteEditorWrapper
from ..qthelper.qtimports import QWidget

class NoteEditDialogWrapper:
  def __init__(self, addCardsOrBrowserDialog):
    """
    Wrapper for the dialog that will contain the TagSelector.
    This could be:
      - add Cards dialog
      - browser dialog
      - edit card dialog
    """
    self._dialog = addCardsOrBrowserDialog

  def getForm(self):
     return self._dialog.form

  def getEditor(self) -> NoteEditorWrapper:
     return NoteEditorWrapper(self._dialog.editor)

  def getWidget(self):
     return self._dialog


  def isEditCurrentDialog(self):
     return (type(self._dialog).__name__ == "EditCurrent")

  def isNoteBrowserDialog(self):
     return (type(self._dialog).__name__ == "Browser")

  def idAddCardsDialog(self):
     return (type(self._dialog).__name__ == "AddCards")

  def closeWithoutSaving(self):
     self._dialog.reject()

  def close(self):
     self._dialog.close()


  def hasAttribute(self, attributeName: str):
     return hasattr(self._dialog, attributeName)

  def setAttribute(self, attributeName: str, value):
    setattr(self._dialog, attributeName, value)




  # These functions below are TS-specific functions.
  # They should not be here, because this class should
  #  only be a wrapper for Anki stuff

  def setCurrentDockWidget(self, dockWidget: QWidget):
     self._dialog.form.tsDockWidget = dockWidget

  def getCurrentDockWidget(self):
     return self._dialog.form.tsDockWidget

