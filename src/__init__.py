
from .config import *
from .main import main

# for making data avaiable all over anki without HDD read/write
# And enablign config-Feature
from aqt import mw # type: ignore
# Enable config in Anki2.1
ankiconfig = mw.addonManager.getConfig(__name__)

main(ankiconfig)

