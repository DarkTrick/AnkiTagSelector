#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------
import datetime

class DTLogger():
    def __init__(self,filename = "DTlogger.log"):
        self._filename: str = filename


    def debug(self,value):
        self._log("Debug: " + value)
        pass

    def _log(self,value):
        with open(self._filename, "a") as file: # appendingmode
            file.writelines(str(datetime.datetime.now()) + ": " + value + "\n")


class DTLoggerMock():
    def __init__(self,filename = None):
        pass
    def debug(self,str):
        pass
    pass
