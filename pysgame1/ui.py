# Though QtXml is not used, it is a hidden import that PyInstaller needs to
# see.
from PySide import QtCore, QtGui, QtUiTools, QtXml
from pysgame1.Ui_MainWindow import Ui_MainWindow

from pysgame1.game import Household, Person, Game

invalid_QModelIndex = QtCore.QModelIndex()
class TreeNode(object):
    """Adapted from
    http://www.hardcoded.net/articles/using_qtreeview_with_qabstractitemmodel.

    This provides a basic shell that can be easily filled in for whatever you
    need."""
    def __init__(self, parent, row):
        self.parent = parent
        self.row = row
        self.subnodes = self._getChildren()

    def _getChildren(self):
        raise NotImplementedError()

class TreeModel(QtCore.QAbstractItemModel):
    """Adapted from
    http://www.hardcoded.net/articles/using_qtreeview_with_qabstractitemmodel.

    This provides a basic shell that can be easily filled in for whatever you
    need."""

    def __init__(self):
        super(TreeModel, self).__init__()
        self.rootNodes = self._getRootNodes()

    def _getRootNodes(self):
        raise NotImplementedError()

    def index(self, row, column, parent):
        if not parent.isValid():
            return self.createIndex(row, column, self.rootNodes[row])
        parentNode = parent.internalPointer()
        return self.createIndex(row, column, parentNode.subnodes[row])

    def parent(self, index):
        if not index.isValid():
            return invalid_QModelIndex
        node = index.internalPointer()
        if node.parent is None:
            return invalid_QModelIndex
        else:
            return self.createIndex(node.parent.row, 0, node.parent)

    def reset(self):
        self.rootNodes = self._getRootNodes()
        super(TreeModel, self).reset(self)

    def rowCount(self, parent):
        if not parent.isValid():
            return len(self.rootNodes)
        node = parent.internalPointer()
        return len(node.subnodes)

class HouseholdNode(TreeNode):

    def __init__(self, household, parent, row):
        self.household = household
        super(HouseholdNode, self).__init__(parent, row)

    def _getChildren(self):
        return [PersonNode(person, self, index)
                for index, person in enumerate(self.household.members)]

class PersonNode(TreeNode):

    def __init__(self, person, parent, row):
        self.person = person
        super(PersonNode, self).__init__(parent, row)

    def _getChildren(self):
        return []


class PeopleTreeModel(TreeModel):
    """First level: Households. Second level: Members of the household."""

    def __init__(self, game):
        self.game = game
        super(PeopleTreeModel, self).__init__()

    def _getRootNodes(self):
        root_nodes = []

        root_nodes += [
                PersonNode(person, None, index)
                for index, person in enumerate(self.game.household.members)]

        root_nodes += [
            HouseholdNode(household, None, index)
                for index, household in enumerate(self.game.other_households,
                    start=index+1)]

        return root_nodes

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return ["Name", "Gender", "Age", "Job"][section]

    def columnCount(self, index=invalid_QModelIndex):
        if not index.isValid():
            return 4

        node = index.internalPointer()
        if isinstance(node, HouseholdNode):
            return 4
        elif isinstance(node, PersonNode):
            return 4
        else:
            return 4

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        node = index.internalPointer()
        col = index.column()

        if role == QtCore.Qt.DisplayRole:
            if isinstance(node, HouseholdNode):
                household = node.household
                if col == 0:
                    return household.name
            elif isinstance(node, PersonNode):
                person = node.person
                if col == 0:
                    return person.name
                elif col == 1:
                    return person.gender
                elif col == 2:
                    return person.age
                elif col == 3:
                    return person.job

    #def sort(self, column, order=QtCore.Qt.AscendingOrder):
    #    key = {
    #            0: lambda person: person.first_name,
    #            1: lambda person: person.surname,
    #            2: lambda person: person.gender,
    #            3: lambda person: person.age,
    #            4: lambda person: person.job,
    #            }[column]
    #    self.people.sort(
    #            key=key,
    #            reverse=order==QtCore.Qt.DescendingOrder)


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.game = Game()

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


