from PySide import QtCore, QtGui, QtUiTools, QtXml
from pysgame1.ui.tree import TreeModel, invalid_QModelIndex

from .HouseholdNode import HouseholdNode
from .PersonNode import PersonNode

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



