gDEFAULT_SPACE_BETWEEN_TAG_FIELDS = 3


# changing default size of TagSelectorArea
gDefaultTagSelectorSizeArea = 30
gDefaultTagSelectorSizeAreaHeight = 250

gDEFAULT_OBJECT_VERSION_NUMBER = 2

#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------


from PyQt5 import QtCore, QtGui # Core for Signals; Gui for gui

import os # for default path of savefile
import pickle # for saving to fs

#from aqt.utils import showInfo
from .logging import *
#gLogger = DTLogger("..\\..\\DTLogger.log")
gLogger = DTLoggerMock()

# ========================================================================
# ========================================================================

"""
We want only one TSGui. Not destroy and rebuild.
"""
class AnkiConnectionPointer:
    def __init__():
        self.dialogPointer = None

    pass

# ========================================================================
# ========================================================================

class TagSelectorItemBaseInterface:
    """ defines functions, that should be implemented by derived classes
        to make sync between gui-datastructure and datastructure easier"""
    def _notYetImplementedException(self):
        raise Exception("implemented by derived class")

    def setTagsString(self, stringValue):
        self._notYetImplementedException()

    def getTagsString(self):
        self._notYetImplementedException()

# ========================================================================
# ========================================================================

class TagSelectorItem(TagSelectorItemBaseInterface):
    """ - dataset of one Item within the list of selectable items
     - savable

     - every data, that should be available for each item goes here"""

    def __init__(self, tagsString = ""):
        # currently we have only one element here, but it might get more
        self.tagsString = tagsString

    def setTagsString(self, stringValue ):
        self.tagsString= stringValue

    def getTagsString(self):
        return self.tagsString

    def toString(self):
        return self.getTagsString()

# ========================================================================
# ========================================================================


""" hast saveable datastructure"""
class TSDataPersistent:
    class PersistanceMgmt:

        @staticmethod
        def clearData(filename = None):
            """@return: True if file was deleted, False otherwise"""
            filename = TSDataPersistent.PersistanceMgmt.getFsFilename(filename)
            try:
                os.remove(filename)
            except:
                return False
            return True
            pass

        @staticmethod
        def loadDataFromFilesystem(filename = None):
            """
            @return: loaded data
                     or None, if no data was loadable
            @param: filename: define a different filename, if you want. Otherwise default is taken
            """
            filename = TSDataPersistent.PersistanceMgmt.getFsFilename(filename)

            gLogger.debug("loadDataFromFilesystem: " + filename)

            loadedTagSelectorData = None
            # only load from FS, if ts doesnt exist already
            fileExists = True
            try:
                file = open( filename, "rb" )
                loadedTagSelectorData = pickle.load(file)
            except:
                fileExists = False

            if(fileExists == True):
                file.close()

                # basically for saving time finding bugs, as pickler doesn't inform about anything:
                if (loadedTagSelectorData.CLASSVERSION != TSDataPersistent().CLASSVERSION):
                    #showInfo('TagSelector Version has changed. Could not load old File.\nCreate new one.')
                    loadedTagSelectorData = None
            else:
                pass # we had nothing to load, so we're empty

            return loadedTagSelectorData


        # --------------------------------------------------------------------
        @staticmethod
        def saveDataToFilesystem(tsData, filename = None):
            """ @return: False, if data could not be saved """
            try:
                filename = TSDataPersistent.PersistanceMgmt.getFsFilename(filename)
                gLogger.debug("saveDataFromFilesystem: " + filename)
                file = open(filename, 'wb')
                pickle.dump(tsData , file)
                file.close()
            except:
                return False

            return True
            pass
        # --------------------------------------------------------------------
        static_PathToConfigFile = ".."
        @staticmethod
        def getFsFilename(filename = None):
            #showInfo("FS was accessed")
            # points to the current profile folder
            thePath = os.path.join(TSDataPersistent.PersistanceMgmt.static_PathToConfigFile,"TagSelectorConfigFileV2.config")
            if(filename == None):
                return thePath
            else:
                return filename
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------


    def __init__(self, initialDataSize = 0):
        # must be nonstatic member in order to work properly!
        self.CLASSVERSION = gDEFAULT_OBJECT_VERSION_NUMBER
        # class-overlapping shared variable

        """ array can be directly manipulated by other classes """
        self.tagSelectorItems =  []
        # initially fill the array
        for i in range(0,initialDataSize-1):
            self.addItem(TagSelectorItem())
        self.dockWidgetData = DockWidgetData()


    def getItemsAsString(self):
        firstItem = True
        ret = "["
        for item in self.getItemsArray():
            if(firstItem == False):
                ret += ","
            else:
                firstItem = False
            ret += item.toString()
            pass
        ret += "]"
        return ret

    def setDockWidgetData(self, dockWidgetData):
        self.dockWidgetData = dockWidgetData

    def addItem(self, tagSelectorItem):
        self.tagSelectorItems.append(tagSelectorItem)

    def getItemsArray(self):
        return self.tagSelectorItems

    def clearItemsData(self):
        self.tagSelectorItems = []

    def getItem(self, index):
        return self.tagSelectorItems[index]

    def getItemCount(self):
        return len(self.tagSelectorItems)

# ========================================================================
# ========================================================================

class DockWidgetData:
    def __init__(self):
        self.position = QtCore.Qt.DockWidgetArea(2) #2 # right side by default
        self.isVisible = True
        self.isFloating = False
        self.floatingPosX = 0
        self.floatingPosY = 0
        self.width = gDefaultTagSelectorSizeArea
        self.height = gDefaultTagSelectorSizeAreaHeight

    def toString(self):
        return "visible: " + str(self.isVisible) + \
                "   isFloating: " + str(self.isFloating)+ \
                "   position: " + str(self.position)

# ========================================================================
# ========================================================================

class ComprehensiveFunctions: # comprehensive = uebergreifend
    @staticmethod
    def addTags(EditorObject, strTags):
        tags = EditorObject.tags

        tags.setText(tags.text() + " " + strTags)
        EditorObject.saveTags()
        #TODO: send signal "lostfocus" would be cleaner! (aqt/editor.py:629)

    # --------------------------------------------------------------------
    @staticmethod
    def _removeSpaceSeperatedStrFromStr(strCurrentTags, strTagsToRemvoe):
        # 1. convert string to array
        # 2. manipulate array
        # 3. convert array to string

        splitDelimiter = " " # TODO: should handle other white-spaces!
        arrayCurrentTags = strCurrentTags.split(splitDelimiter)
        arrayNewTags = strCurrentTags.split(splitDelimiter)
        arrayToRemove = strTagsToRemvoe.split(splitDelimiter)

        # Remove all tags specified - Bugfix: CASE INSENSITIVE
        for oneTagToRemove in arrayToRemove:
            for currentTag in arrayCurrentTags:
                if(currentTag.lower() == oneTagToRemove.lower()):
                    arrayNewTags.remove(currentTag)

        return " ".join(arrayNewTags)

    # ---------------------------------------------------------------------
    @staticmethod
    def removeTags(EditorObject, strTagsToRemove):
        currentTags = EditorObject.tags.text()
        newTags = ComprehensiveFunctions._removeSpaceSeperatedStrFromStr(
            currentTags, strTagsToRemove)
        EditorObject.tags.setText(newTags)

        # do we need this?
        # EditorObject.saveTags()
        #TODO: send signal "lostfocus" would be cleaner! (aqt/editor.py:629)
        pass

    # ---------------------------------------------------------------------
    @staticmethod
    def replaceAllWhitespaces(sourceString, replacerString):
        ret = sourceString
        ret = ret.replace(u'\u00A0',replacerString)
        ret = ret.replace("\t",replacerString)
        ret = ret.replace(" ",replacerString)
        ret = ret.replace(u'\u3000',replacerString)
        return ret
        pass
    # --------------------------------------------------------------------


# ========================================================================
# ========================================================================

