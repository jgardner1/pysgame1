# Though QtXml is not used, it is a hidden import that PyInstaller needs to
# see.
from PySide import QtCore, QtGui, QtUiTools, QtXml
from pysgame1.Ui_MainWindow import Ui_MainWindow
from pysgame1.ui.PeopleTreeModel import PeopleTreeModel

class MainWindow(QtGui.QMainWindow):
    def __init__(self, game, parent=None):
        super(MainWindow, self).__init__(parent)

        self.game = game

        # Load main.ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.input.returnPressed.connect(self.new_input)

        self.ui.actionEndTurn.activated.connect(self.game.end_turn)
        self.ui.actionShowStatus.activated.connect(self.game.show_status)

        self.ui.peopleTreeView.setModel(PeopleTreeModel(self.game))
        self.ui.peopleTreeView.setUniformRowHeights(True)
        #self.ui.peopleTreeView.setSortingEnabled(True)

        self.ui.endTurnButton.clicked.connect(self.game.end_turn)

        self.game.output.connect(self.ui.output.append)

    def new_input(self):
        text = self.ui.input.text()
        self.ui.input.setText("")

        self.ui.output.append("You entered: "+text)
        self.game.end_turn()



