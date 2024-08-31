
from aqt import mw # type: ignore
from typing import Union
from ..datapersister.tsdatapersister import TSDataPersistent
from ..config import *

def getTsDataFromAnkiMw() -> Union[TSDataPersistent, None]:
    if(hasattr(mw,"tagSelectorData")):
        return mw.tagSelectorData
    return None

def isAnkiDataInMwAvailable():
    if(hasattr(mw,gITEM_NAME_OF_OBJECT_IN_ANKI_MW)):
        if(not (None == getTsDataFromAnkiMw())):
            return True
    return False

def setTsDataInAnkiMw(tsData):
    mw.tagSelectorData = tsData