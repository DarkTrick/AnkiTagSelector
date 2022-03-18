#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------
import datetime
class DTLogger():
    def __init__(self,filename = None):
        self._filename = filename
        if(None == self._filename):
            self._filename = "DTlogger.log"


    def debug(self,value):
        self._log("Debug: " + value)
        pass

    def _log(self,value):
        self._file = open(self._filename, "a") # appendingmode
        self._file.writelines(str(datetime.datetime.now()) + ": " + value + "\n")
        #self._file.writelines(value)

        self._file.close()
        pass

class DTLoggerMock():
    def __init__(self,filename = None):
        pass
    def debug(self,str):
        pass
    pass
