#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------


from ..tsutils.glogger import gLogger
import os
import pickle
from typing import Union
from ..config import *
from ..datamodel.tagselectoritem import TagSelectorItem
from ..datamodel.dockwidgetdata import DockWidgetData

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
        def loadDataFromFilesystem(filename = None) -> Union["TSDataPersistent", None]:
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

            if(fileExists == True and loadedTagSelectorData is not None):
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


    def getItemsAsString(self) -> str:
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
