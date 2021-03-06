#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'alex barnes'

import random
import mechanics
import mobs


class maps(object):
    __str__ = "Base class for generating and managing rooms in pygame."

    difficulty = 0
    desc = ""
    exits = 0
    monCount = 0
    doorDiffs = [999,999,999,999]

    def __init__(self):
        "This is an abstract base class and should not be used directly"
        raise NotImplementedError

    def rollChance(self, player):
        """
        Desc: rolls and enacts chance events.
        Called by: Main game loop in game.

        Notes:
        chance events have a chance of occurring once per room.
        chance events occur after a battle and before the next door is chosen.
        """
        chance = mechanics.roll100()
        # scaffold for chance events
        if chance in range(1, 25):
            # nothing. 25% chance of no event.
            pass
        elif chance in range(26, 30):
            if player.chp < player.hp:
                print "\nThis room has a small fountain containing clean water. You quickly drink it, restoring your health."
                if (player.chp + 50) <= player.hp:
                    player.chp += 50
                else:
                    player.chp = player.hp
            else:
                print "\nThis room has a small fountain containing clean water. You quickly drink it, but your health is already full."
            print player.showHP()

        elif chance in range(31, 35):
            print "\nAn imp throws a rock at you before disappearing in a puff of smoke."
            player.chp -= 5
            print player.showHP()

        elif chance in range(36, 50):
            pass

        elif chance in (51, 52):
            print "\nYou find a piece of armor on the floor in this room. You strap it onto yourself as best you can. You feel more protected. (Armor increased to {}).".format(
                player.arm + 2)
            player.arm += 2

        elif chance in range(53, 96):
            pass

        elif chance in (97, 98):
            # Keep this in mind once levels are implemented
            print "\nA lost spirit appears to you. 'Hail, {}. I perished here, like many before me. I give you my blessing, that you may find freedom again'. As the spirit disappears, you feel slightly more healthy. (Health permanently increased to {}).".format(player.name, player.hp + 30)
            player.hp += 30
            if (player.chp + 30) <= player.hp:
                player.chp += 30
            else:
                player.chp = player.hp
            print player.showHP()

        elif chance == 99:
            print "\nYou find a pair of leather shoes to protect your bare feet, allowing you to move slightly more quickly. (Agility increased to {}.)".format(
                player.agi + 1)
            player.agi += 1

        elif chance == 100:
            pass
            # Some very rare event

    def rollDiff(self):
        """
        Desc: determines the difficulty of a room.
        Called by: room.maps.rollNextRooms()

        Notes:
        the difficulty will be used to modify monster stats, and perhaps item drops.
        it uses ranges so that chances can be modified easily and is then bucketed for use.
        """
        diffRoll = mechanics.roll100()
        if diffRoll in range(1, 25):
            return 0
        elif diffRoll in range(26, 75):
            return 1
        elif diffRoll in range(76, 90):
            return 2
        else:
            return 3

    def rollExits(self):
        """
        Desc: determines how many exits a given room has.
        Called by: room.maps.miscRoom.__init__()
        """
        exitsRoll = mechanics.roll100()
        # exits are bucketed similar to difficulty
        if exitsRoll in range(1, 5):
            return 1
        elif exitsRoll in range(6, 55):
            return 2
        elif exitsRoll in range(56, 90):
            return 3
        else:
            return 4

    def rollNextRooms(self):
        """
        Desc: chooses the difficulty for each next door.
        Called by: room.maps.miscRoom.__init__()

        Notes:
        ensures that each door is a different difficulty."""
        self.doorDiffs[0] = self.rollDiff()
        while self.doorDiffs[1] == 999 or self.doorDiffs[1] == self.doorDiffs[0]:
            self.doorDiffs[1] = self.rollDiff()
        while self.doorDiffs[2] == 999 or self.doorDiffs[2] == self.doorDiffs[0] or self.doorDiffs[2] == self.doorDiffs[1]:
            self.doorDiffs[2] = self.rollDiff()
        while self.doorDiffs[3] == 999 or self.doorDiffs[3] == self.doorDiffs[0] or self.doorDiffs[3] == self.doorDiffs[1] or self.doorDiffs[3] == self.doorDiffs[2]:
            self.doorDiffs[3] = self.rollDiff()

    def doorDesc(self, diff):
        """
        Desc: returns door descriptions
        Called by: room.maps.nextRooms()
        """
        if diff == 0:
            return "This wooden door feels warm and inviting."
        elif diff == 1:
            return "This is a solid wooden door."
        elif diff == 2:
            return "You hear the sounds of some great beast behind this steel door."
        else:
            return "Blood seeps beneath this black stone door, and the sounds of something angry emanate from within."

    def nextRooms(self, exits):
        """
        Desc: displays exits for the next rooms.
        Called by: room.maps.miscRoom.__init__() and main game loop in game
        """
        if exits > 1:
            print ""
            print "This room has {} exits.".format(exits)
        else:
            print ""
            print "This room only has 1 exit."
        print "1) {}".format(self.doorDesc(self.doorDiffs[0]))
        if exits > 1:
            print "2) {}".format(self.doorDesc(self.doorDiffs[1]))
        if exits > 2:
            print "3) {}".format(self.doorDesc(self.doorDiffs[2]))
        if exits > 3:
            print "4) {}".format(self.doorDesc(self.doorDiffs[3]))


    def enter(self, player):
        """
        Desc: takes actions when a player enters a room.
        Called by: main game loop in game

        Notes:
        i would like to move combat into this, but it needs to interrupt the regular game loop, so it is currently implemented there.
        """
        print ""
        print self.desc
        player.roomCt += 1
        monster = mobs.pickMob(self.difficulty)
        if type(monster) != type(None):
            self.monCount += 1
            print monster.desc
            print ""
            return monster
        else:
            print "You appear to be alone here."
            return None


class miscRoom(maps):
    def rollDesc(self):
        """
        Desc: randomly assigned descriptions to rooms.
        Called by: room.maps.miscRoom.__init__()

        Notes:
        in the future, I plan to move these out to a flat file which will be read from.
        """
        descRoll = random.randint(0, 4)
        if descRoll == 0:
            self.desc = "You walk through the door into a stone corridor, dimly lit by a flickering torch on the wall. Filthy water drips from the ceiling, and the walls are cast in shadows."
        elif descRoll == 1:
            self.desc = "You enter into a dark room. You can barely make out a partially collapsed wall. The smell of earth fills your nose."
        elif descRoll == 2:
            self.desc = "You walk into a warm room. It appears there was a fire burning here just moments ago."
        elif descRoll == 3:
            self.desc = "You walk through the door into a room strewn with the remains of a bloody battle. Your feet stick to the floor, and your nose is filled with the smell of death."
        elif descRoll == 4:
            self.desc = "Your enter into what appears to have been a great hall, long ago. The room has been heavily looted, but the high ceilings provide a stark contrast to the cramped tunnels you have been traveling."
        else:
            self.desc = "There appears to be a problem generating a description."

    def __init__(self, diff):
        self.difficulty = diff
        self.rollDesc()
        self.exits = self.rollExits()
        self.rollNextRooms()


class startRoom(maps):
    def __init__(self):
        self.exits = 1
        self.desc = "You awaken in a cramped stone cell. Your head aches and you have no memory of how you came to be here. There are a few items bundled together in the center of the room, and the door hangs slightly open. You hear the distant sound of creatures in the darkness beyond."
        self.doorDiffs[0] = 1
        self.difficulty = -1
        pass


class endRoom(maps):
    """
    Desc: this is the room that must be reached in order to win the game.

    Notes:
    I would like to build a leader board at some points.
    """
    def __init__(self, player):
        self.desc = "\nYou step through the door and are immediately blinded by bright light. You smell fresh air and feel a breeze on your bloody and bruised face. As your eyes adjust, you see stone steps leading up to the surface. You've survived."
        self.difficulty = -1
        print self.desc
        player.win()


def main():
    room1 = miscRoom(1)


    print "Room debug info:"
    print "Difficulty - {},".format(room1.difficulty)
    print "Exits - {}.".format(room1.exits)
    print "Door 1 diff: {}".format(room1.doorDiffs[0])
    print "Door 2 diff: {}".format(room1.doorDiffs[1])
    print "Door 3 diff: {}".format(room1.doorDiffs[2])
    print "Door 4 diff: {}".format(room1.doorDiffs[3])


if __name__ == "__main__":
    main()
