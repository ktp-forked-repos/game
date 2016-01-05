#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__author__ = 'alex8955'

import player
import room


def main():
    currentRoom = room.startRoom()

    print "Welcome to Pygame."
    print ""
    char = player.player()

    while char.hp > 0:
        currentRoom.enter(currentRoom)
        currentRoom.nextRooms(currentRoom.exits)
        currentRoom = currentRoom.chooseDoor(currentRoom.door1diff, currentRoom.door2diff, currentRoom.door3diff, currentRoom.door4diff, currentRoom.exits)

    if char.hp < 1:
        print "You have died, like many before you.ß"


if __name__ == "__main__":
    main()