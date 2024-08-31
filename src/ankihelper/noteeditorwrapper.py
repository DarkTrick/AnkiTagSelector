
from .notewrapper import NoteWrapper


class NoteEditorWrapper:
  def __init__(self, noteEditor):
    """
    Wrapper for Anki's Editor.

    Goal:
      1. Make up for inconvenient interfaces.
      2. Provide intellisense for functions the Tagselector uses

    @Args:
      - noteeditor: Anki's aqtEditor
    """


    self._noteEditor = noteEditor

  def tagsChanged(self):
    """Inform the editor that the tags changed in order
       to load data onto the screen
    """
    self._noteEditor.loadNote()

  def getNote(self) -> NoteWrapper:
    return NoteWrapper(self._noteEditor.note)
