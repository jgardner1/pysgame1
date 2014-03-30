from PySide import QtCore, QtGui, QtUiTools, QtXml
from pysgame1.ui.tree import TreeNode, TreeModel, invalid_QModelIndex

class PersonNode(TreeNode):

    def __init__(self, person, parent, row):
        self.person = person
        super(PersonNode, self).__init__(parent, row)

    def _getChildren(self):
        return []

