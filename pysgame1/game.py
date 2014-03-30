import random
import weakref

from pysgame1.names import female_names, male_names, surnames
from pysgame1.util import clamp

from PySide import QtCore

class Household(object):
    """A Household has members. Each household has its own store of food and
    gold and such. People tend to eat together and share resources within a
    household."""

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
    """A Person is a person.

    gender: M or F
    age: An int
    first_name: Their first name, based on their gender.
    surname: Their family name.
    job: Their current job.
    household: The household they belong to (weakref.) Persons always belong
        to a house. If they break away, they form their own house.
    game: weakref to the game object.
    you: Whether this is the main character.
    name: (prop) The calculated name. Appends '(you)' if it is you.
    """

    def __init__(self, household, game, gender=None):
        self.gender = gender or random.choice(['M','F'])
        self.age = int(min(65, max(0, random.gauss(25, 10))))
        self.first_name = random.choice(male_names if self.gender == 'M' else
                female_names)
        self.surname = random.choice(surnames)
        self.job = "gather"
        self.household = weakref.proxy(household)
        self.game = weakref.proxy(game)
        self.you = False

    @property
    def name(self):
        name = "{} {}".format(self.first_name, self.surname)
        if self.you:
            return name + ' (you)'
        else:
            return name

    def __repr__(self):
        return "<Person %s %s (%s) age %d at 0x%#d>" % (
                self.first_name,
                self.surname,
                self.gender,
                self.age,
                id(self))

    def do_job(self):
        """Applies the job and reaps the effects."""
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
    """The main game object."""
    output = QtCore.Signal(str)
    def __init__(self):
        super(Game, self).__init__()

        # Your household
        self.household = Household(self)
        self.age = clamp(18, 25, random.gauss(20, 3))

        # You
        self.you = Person(self.household, self, 'M')
        self.you.job = "administer"
        self.you.you = True

        self.other_households = []
        self.household.members = [self.you]+[Person(self.household, self) for _ in xrange(5)]

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
