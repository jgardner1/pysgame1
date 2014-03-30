from PySide import QtCore, QtGui, QtUiTools, QtXml
from pysgame1.ui.tree import TreeNode
from .PersonNode import PersonNode

class HouseholdNode(TreeNode):

    def __init__(self, household, parent, row):
        self.household = household
        super(HouseholdNode, self).__init__(parent, row)

    def _getChildren(self):
        return [PersonNode(person, self, index)
                for index, person in enumerate(self.household.members)]
