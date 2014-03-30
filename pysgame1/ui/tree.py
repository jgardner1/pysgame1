"""TreeNode and TreeModel from
http://www.hardcoded.net/articles/using_qtreeview_with_qabstractitemmodel.
"""
from PySide import QtCore, QtGui, QtUiTools, QtXml

invalid_QModelIndex = QtCore.QModelIndex()
class TreeNode(object):
    """A Node in the tree view has a parent, a row, and subnodes."""
    def __init__(self, parent, row):
        self.parent = parent
        self.row = row
        self.subnodes = self._getChildren()

    def _getChildren(self):
        """Override this and return the subnodes if any."""
        raise NotImplementedError()

class TreeModel(QtCore.QAbstractItemModel):
    """A TreeModel has root nodes."""

    def __init__(self):
        super(TreeModel, self).__init__()
        self.rootNodes = self._getRootNodes()

    def _getRootNodes(self):
        """Override this and return the root nodes."""
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

