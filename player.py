#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__author__ = 'alex barnes'

import random


class player(object):
    """
    This object represents the player within the game. It handles creation and storage of all player statistics.
    """

    strg = agi = end = hp = chp = arm = ap = 0
    name = ""

    def roll_stats(self):
        "generates player stats"
        roll = {'strg': 0, 'agi': 0, 'end': 0}
        roll['strg'] = random.randint(1, 18)
        roll['agi'] = random.randint(1, 18)
        roll['end'] = random.randint(1, 18)
        # make sure total stars are between 15 and 45, if not reroll
        while (roll['strg'] + roll['agi'] + roll['end']) >= 45 or (roll['strg'] + roll['agi'] + roll['end']) <= 25 or \
                        roll['strg'] < 4 or roll['agi'] < 4 or roll['end'] < 4:
            roll = self.roll_stats()
        return roll

    def __str__(self):
        return "Your stats are: \nStrength: {} \nAgility: {} \nEndurance: {} \nHit Points: {} \nArmor: {}".format(
            self.strg, self.agi, self.end, self.hp, self.arm)

    def __init__(self):
        print "Creating character."
        print ""
        self.name = str(raw_input("What is your name, traveler? "))

        print "You will have three rolls to choose from."
        print "Rolling stats."

        roll1 = self.roll_stats()
        roll2 = self.roll_stats()
        roll3 = self.roll_stats()

        # Debug stats. Special name 'AlexRocks' sets stats very high to allow for in-game testing with super stats.
        if self.name == 'AlexRocks':
            roll1 = {'strg': 100, 'agi': 100, 'end': 100}

        print "1) Str: {}, Agi: {}, End: {}".format(roll1['strg'], roll1['agi'], roll1['end'])
        print "2) Str: {}, Agi: {}, End: {}".format(roll2['strg'], roll2['agi'], roll2['end'])
        print "3) Str: {}, Agi: {}, End: {}".format(roll3['strg'], roll3['agi'], roll3['end'])

        choice = int(raw_input("Which option will you choose?: "))
        while choice not in (1, 2, 3):
            choice = int(raw_input("Please choose either 1, 2 or 3: "))

        if choice == 1:
            self.strg = roll1['strg']
            self.agi = roll1['agi']
            self.end = roll1['end']
        elif choice == 2:
            self.strg = roll2['strg']
            self.agi = roll2['agi']
            self.end = roll2['end']
        else:
            self.strg = roll3['strg']
            self.agi = roll3['agi']
            self.end = roll3['end']

        # set secondary stats based on primary
        self.hp = self.chp = 100 + (self.end * 5)
        if self.end % 2 == 0:
            self.arm = self.end / 2
        else:
            self.arm = (self.end - 1) / 2

        print ""
        print "Hail, {}.".format(self.name)
        print ""
        print self


def main():
    char = player()


if __name__ == "__main__":
    main()
