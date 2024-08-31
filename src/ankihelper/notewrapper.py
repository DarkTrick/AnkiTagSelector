
class NoteWrapper:
  def __init__(self, ankiNote):
    """
    Wrapper for an Anki Note.

    This wrapper tries to make up for inconvenient interfaces.

    @Args:
      - ankiNote: `Note` object from Anki
    """
    self._note = ankiNote

  def add_tag(self, tag: str):
    self._note.add_tag(tag)

    # Just UX: remove duplicates before they appear on screen
    #  But do so in a way that will note crash the whole addon.
    try:
      if(isinstance(self._note.tags, list)):
        self._note.tags = list(set(self._note.tags))
    except:
      pass

  def add_tags_from_string_list(self, tags: str):
    """example: `tags="a b c"`"""
    for tag in tags.split(" "):
        self.add_tag(tag)

  def remove_tag(self, tag: str):
    self._note.remove_tag(tag)

  def remove_tags_from_string_list(self, tags: str):
    """example: `tags="a b c"`"""
    for tag in tags.split(" "):
        self.remove_tag(tag)

