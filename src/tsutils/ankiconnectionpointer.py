#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------

class AnkiConnectionPointer:
    """
    We want only one TSGui. Not destroy and rebuild.
    """
    def __init__(self):
        self.dialogPointer = None

    pass
