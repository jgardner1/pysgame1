#!/usr/bin/env python2

from pysgame1.ui import MainWindow
from PySide import QtGui

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
