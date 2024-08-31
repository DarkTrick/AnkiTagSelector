from .tsutils.easyconfig import *
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

# ===============================================================
# ====== for special colors,  ===================================
# ======   remove the marked "return" below and set colors ======
# ===============================================================
from .qthelper.qtimports import QColor
from .qthelper.qtimports import blue

BG_COLOR_TITLE_BAR = QColor(120,120,255,255)
TS_BG_COLOR = QColor(120,255,255,120)
BG_COLOR_TAGS = QColor(0,255,0,20)

def changeBGColor(widget, color = blue):
    return # remove this line to make colors work

    if(color == None):
        return
    p = widget.palette()
    p.setColor(widget.backgroundRole(), color)
    widget.setPalette(p)
    widget.setAutoFillBackground(True)





# ======================
# ======= Design =======
# ======================

# this will be the entry name under Tools->Add-Ons
gNAME_OF_THIS_FILE = 'TagSelector'
gAddonNamePrettyString = "Tag Selector"



gDEFAULT_SPACE_BETWEEN_TAG_FIELDS = 3

# For changing the number of Input fields, change this value:
defaultNumberOfInputFields = 1

# changing default size of TagSelectorArea
gDefaultTagSelectorSizeArea = 170

# changing default size of TagSelectorArea
gDefaultTagSelectorSizeArea = 30
gDefaultTagSelectorSizeAreaHeight = 250



# ==============================
# ====== Internal stuff ========
# ==============================
gDEFAULT_OBJECT_VERSION_NUMBER = 2

# ==============================================================================
""" reason for this? Don't spread "mw.tagSelectorData" calls all over the code
    with the need to change, if we make a change. Or even worse: spread typos"""
gITEM_NAME_OF_OBJECT_IN_ANKI_MW = "tagSelectorData"
gITEM_NAME_OF_OBJECT_IN_DIALOG = "tagSelector"


