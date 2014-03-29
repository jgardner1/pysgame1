#!/usr/bin/env python

import random, weakref

# Though QtXml is not used, it is a hidden import that PyInstaller needs to
# see.
from PySide import QtCore, QtGui, QtUiTools, QtXml
from Ui_MainWindow import Ui_MainWindow
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_names(filename):
    names = file(resource_path(filename)).read().split('\n')
    names = [name.strip() for name in names]
    names = [name for name in names if name]
    return names

female_names = load_names("female_names.txt")
male_names = load_names("male_names.txt")
surnames = load_names("surnames.txt")

class Household(object):

    def __init__(self, game):
        self.food = 0
        self.gold = 0
        self.members = []
        self.name = "Household"
        self.game = weakref.proxy(game)

    def do_jobs(self):
        for person in self.members:
            person.do_job()

    def eat(self):
        """Eat the food in the house.
        - The owners of the house will eat more food than the servants, but
          not so much that the servants will starve. Also, pregnant women get
          fed, children get fed, warriors get fed, farmers get fed before
          others.
        - The food is divided up equally, unless some servants or household
          members are dishonest.
        - To prevent starvation, the household will look at how much food is
          stored and ration appropriately.

        How much food?
        - 1 pounds of food/day: Not starving.
        - 2 pounds of food/day: Fed.
        - 4 pounds of food/day: Very well fed.
        - Can't really go beyond 4 pounds.
        """
        if len(self.members) == 0:
            # Nobody is going to eat anything.
            return

        # Look at the amount of food, and divide by 12. They're planning
        # ahead.
        one_day = self.food / (180.0)
        self.game.output.emit("One day of the food for the next 6 months is {:0.2f}".format(one_day))

        # Divide by members of the household
        per_member = one_day / len(self.members)
        self.game.output.emit("Per person: {:0.2f}".format(per_member))

        if per_member < 1.0:
            self.game.output.emit("This is below starvation level. Forcing to 1 lb.")
            per_member = 1.0
        elif per_member > 4.0:
            self.game.output.emit("This is way too much food. Limiting to 4 lbs.")
            per_member = 4.0

        eaten = len(self.members) * per_member
        self.game.output.emit("Eaten {:0.2f} lbs of food.".format(eaten))

        self.food -= eaten


class Person(object):
    
    def __init__(self, household, game, gender=None):
        self.gender = gender or random.choice(['M','F'])
        self.age = int(min(65, max(0, random.gauss(25, 10))))
        self.first_name = random.choice(male_names if self.gender == 'M' else
                female_names)
        self.surname = random.choice(surnames)
        self.job = "gather"
        self.household = weakref.proxy(household)
        self.game = weakref.proxy(game)

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.surname)

    def __repr__(self):
        return "<Person %s %s (%s) age %d at 0x%#d>" % (
                self.first_name,
                self.surname,
                self.gender,
                self.age,
                id(self))

    def do_job(self):
        if self.job == "gather":
            # Go out into the woods and find food in bushes and such.
            # Should vary based on the time of year. Summer is the most
            # productive time.
            found_food = max(0, random.gauss(10, 5))
            self.game.output.emit("{} found {:0.2f} food.".format(self.name,
                found_food))
            self.household.food += found_food
        else:
            self.game.output.emit("{} doesn't know how to {}.".format(self.name, self.job))
	
class Game(QtCore.QObject):
    output = QtCore.Signal(str)
    def __init__(self):
        super(Game, self).__init__()
        self.household = Household(self)
        self.other_households = []
        self.household.members = [Person(self.household, self) for _ in xrange(5)]

    def end_turn(self):
        #self.citizens += int(self.citizens*0.2+0.5)
        self.output.emit("End turn from Game")
        self.show_status()

        # Generate food
        self.do_jobs()

        # Eat food
        self.eat()

    def do_jobs(self):
        """Goes through each individual and has them perform their job.
        Applies the results of their labor to their household and
        community."""
        for household in [self.household]+self.other_households:
            household.do_jobs()

    def eat(self):
        for household in [self.household]+self.other_households:
            household.eat()

    def show_status(self):
        self.output.emit("You have {} members of your household, {} food and {} gold.".format(
            len(self.household.members),
            self.household.food,
            self.household.gold))

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


        



    
    



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
