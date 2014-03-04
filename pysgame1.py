#!/usr/bin/env python

from PySide import QtCore, QtGui, QtUiTools
from Ui_MainWindow import Ui_MainWindow

class Game(object):
    def __init__(self):
        self.citizens = 20
        self.gold = 0
        self.buildings = {}


    def end_turn(self):
        self.citizens += int(self.citizens*0.2+0.5)

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.game = Game()

        # Load main.ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.input.returnPressed.connect(self.new_input)

        self.show_status()

        self.ui.actionEndTurn.activated.connect(self.end_turn)
        self.ui.actionShowStatus.activated.connect(self.show_status)

    def end_turn(self):
        self.game.end_turn()
        self.show_status()

    def new_input(self):
        text = self.ui.input.text()
        self.ui.input.setText("")

        self.ui.output.append("You entered: "+text)
        self.game.end_turn()
        self.show_status()

    def show_status(self):
        self.ui.output.append("You have {} citizens, {} gold and {} buildings.".format(
                self.game.citizens or 'no',
                self.game.gold or 'no',
                self.game.buildings,
            ))

        



    
    



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
