#-------------------------------------------------------------------------------
# Name:        TagSelector                  # Author:      DarkTrick
# Copyright:   (c) DarkTrick since 2016     # Licence:     CC-BY
#-------------------------------------------------------------------------------

"""
Wrapper for importing stuff from QT from various verions

I know that Anki is supposedly providing
this layer, but I didnt get it to work.
"""

# detect qt version
version = None

try:
  from PyQt6 import QtCore
  version = "qt6"
except:
  from PyQt5 import QtCore
  version = "qt5"

if(version == "qt6"):
  # first try to get Qt6 stuff

  from PyQt6 import QtCore, QtGui # Core for Signals; Gui for gui
  from PyQt6.QtCore import Qt
  from PyQt6.QtGui import QAction
  from PyQt6.QtWidgets import QMainWindow
  from PyQt6.QtWidgets import QWidget

  from PyQt6.QtWidgets import QMenu
  from PyQt6.QtWidgets import QDockWidget
  from PyQt6.QtWidgets import QLineEdit
  from PyQt6.QtWidgets import QCheckBox
  from PyQt6.QtWidgets import QLabel
  from PyQt6.QtWidgets import QVBoxLayout
  from PyQt6.QtWidgets import QHBoxLayout

  from PyQt6.QtGui import QColor
  blue = Qt.GlobalColor.blue

  Qt_AlignTop = Qt.AlignmentFlag.AlignTop
  Qt_CustomContextMenu = Qt.ContextMenuPolicy.CustomContextMenu

if (version == "qt5"):

  # if that doesnt help, try to get
  #  Qt5 stuff next
  from PyQt5 import QtCore, QtGui # Core for Signals; Gui for gui
  from PyQt5.QtCore import Qt
  from PyQt5.QtWidgets import QAction
  from PyQt5.QtWidgets import QMainWindow
  from PyQt5.QtWidgets import QWidget


  # QMenu: create compatibility to PyQt6
  from PyQt5.QtWidgets import QMenu as _QMenu
  class QMenu(_QMenu):
    def exec(self, a):
      self._exec(a)


  from PyQt5.QtWidgets import QDockWidget
  from PyQt5.QtWidgets import QLineEdit
  from PyQt5.QtWidgets import QCheckBox
  from PyQt5.QtWidgets import QLabel
  from PyQt5.QtWidgets import QVBoxLayout
  from PyQt5.QtWidgets import QHBoxLayout

  from PyQt5.QtGui import QColor
  blue = Qt.GlobalColor.blue

  Qt_AlignTop = Qt.AlignTop
  Qt_CustomContextMenu = QtCore.Qt.CustomContextMenu
