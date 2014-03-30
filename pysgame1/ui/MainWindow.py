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

        # When they press enter/return on the input textbox, we will process
        # that input.
        self.ui.input.returnPressed.connect(self.new_input)

        # Whenever they select 'end turn' from the menu, we will end the turn.
        self.ui.actionEndTurn.activated.connect(self.game.end_turn)

        # Whenever they select 'show status' from the menu, we will show the
        # status.
        self.ui.actionShowStatus.activated.connect(self.game.show_status)

        # Set the people tree up with the data.
        self.ui.peopleTreeView.setModel(PeopleTreeModel(self.game))

        # This will make displaying lots of people much faster.
        self.ui.peopleTreeView.setUniformRowHeights(True)
        #self.ui.peopleTreeView.setSortingEnabled(True)

        # Whenever the end turn button is clicked, end the turn.
        self.ui.endTurnButton.clicked.connect(self.game.end_turn)

        # When the game has output, have it display in the output window.
        self.game.output.connect(self.ui.output.append)

    def new_input(self):
        # Gather the text.
        text = self.ui.input.text()

        # Set the text input to blank for the next command.
        self.ui.input.setText("")

        self.ui.output.append("You entered: "+text)

        # TODO: Connect the input to the game object.

        # End the turn. TODO: Not every input will end the turn!
        self.game.end_turn()



