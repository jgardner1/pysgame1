#!/usr/bin/env python

import random

from PySide import QtCore, QtGui, QtUiTools
from Ui_MainWindow import Ui_MainWindow

female_names = file("female_names.txt").read().split('\n')
male_names = file("male_names.txt").read().split('\n')
surnames = file("surnames.txt").read().split('\n')

class Person(object):
    
    def __init__(self):
        self.gender = random.choice(['M','F'])
        self.age = int(min(65, max(0, random.gauss(25, 10))))
        self.first_name = random.choice(male_names if self.gender == 'M' else
                female_names)
        self.surname = random.choice(surnames)
        self.job = "gather"

    def __repr__(self):
        return "<Person %s %s (%s) age %d at 0x%#d>" % (
                self.first_name,
                self.surname,
                self.gender,
                self.age,
                id(self))
        
	
class Game(object):
    def __init__(self):
        self.citizens = [Person() for _ in xrange(5000)]
        self.gold = 0
        self.buildings = {}

    def end_turn(self):
        self.citizens += int(self.citizens*0.2+0.5)


invalid_QModelIndex = QtCore.QModelIndex()
class PeopleTreeViewModel(QtCore.QAbstractItemModel):

    def __init__(self, people):
        super(PeopleTreeViewModel, self).__init__()

        self.people = people

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return ["Given Name", "Surname", "Gender", "Age", "Job"][section]

    def columnCount(self, index=invalid_QModelIndex):
        return 5

    def index(self, row, column, parent=invalid_QModelIndex):
        """Returns the index of the item in the model specified by the given
        row, column, and parent index."""
        # Call createIndex to generate model indexes that other components can
        # use to refer to items in your model.

        if parent.isValid():
            return invalid_QModelIndex()
        else:
            index = self.createIndex(row, column, self.people[row])
            return index

    def hasChildren(self, index=invalid_QModelIndex):
        if index.isValid():
            return False
        else:
            return True


    def parent(self, index):
        """Returns the parent of the model item with the given index. If the
        item has no parent, an invalid QModelIndex is returned."""
        node = invalid_QModelIndex
        #if index.isValid():
        #    nodeS = index.internalPointer()
        #    parent = nodeS.parent
        #    if parent is not None:
        #        node = self.__createIndex(parent.position(), 0, parent)

        return node

    def rowCount(self, index=invalid_QModelIndex):
        node = index.internalPointer()
        if node is None:
            return len(self.people)
        else:
            return 1

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            person = index.internalPointer()
            result = [person.first_name, person.surname, person.gender, person.age,
                    person.job][index.column()]

            return result

    def sort(self, column, order=QtCore.Qt.AscendingOrder):
        key = {
                0: lambda person: person.first_name,
                1: lambda person: person.surname,
                2: lambda person: person.gender,
                3: lambda person: person.age,
                4: lambda person: person.job,
                }[column]
        self.people.sort(
                key=key,
                reverse=order==QtCore.Qt.DescendingOrder)


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

        self.ui.peopleTreeView.setModel(PeopleTreeViewModel(self.game.citizens))
        self.ui.peopleTreeView.setUniformRowHeights(True)
        self.ui.peopleTreeView.setSortingEnabled(True)

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
                len(self.game.citizens) or 'no',
                self.game.gold or 'no',
                self.game.buildings,
            ))

        



    
    



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
