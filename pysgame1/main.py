"""The main game loop. Combines it all together."""

import sys
from PySide import QtGui

from pysgame1.ui import MainWindow
from pysgame1.game import Game

def main():
    # Create the QApplication. This holds the main loop.
    app = QtGui.QApplication(sys.argv)

    # Create the game. It is entirely independent of the UI.
    game = Game()

    # Create a MainWindow with the subject of the game.
    mw = MainWindow(game)
    mw.show()

    # Run the main loop and exit when it is done with the exit code it
    # returns.
    sys.exit(app.exec_())
