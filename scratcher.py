#!./env/bin/python

import math
import nxt.locator

from nxt.motor import *
from collections import namedtuple

from threading import Thread

# The wheel has a circumference of 6 cm averaged over 10 turns.
# The diameter of 1.9 agrees with the result.
# 60 degree turn = 1 cm.


# From http://en.wikipedia.org/wiki/Trilateration.
# Motor A is 0, 0, 0
# Motor B is 0, D, 0
# Motor C is I, J, 0
D = 32.0
I = D / 2
J = 0.86 * D

# Orthocenter: 18.5

Motors = namedtuple("Motors", "A, B, C")


def radii_to_cartesian(r1, r2, r3):
    """Use trilateration to convert cartesian coordinates to radii."""
    x = (r1 ** 2 - r2 ** 2 + D ** 2) / (2 * D)
    y = ((r1 ** 2 - r3 ** 2 + I ** 2 + J ** 2) / (2 * J)) - ((I * x) / J)
    z = math.sqrt(abs(r1 ** 2 - x ** 2 - y ** 2))

    return x, y, z


def cartesian_to_radii(x, y, z):
    """Use trilateration to convert cartesian coordinates to radii."""
    r1 = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    r2 = math.sqrt((x - D) ** 2 + y ** 2 + z ** 2)
    r3 = math.sqrt((x - I) ** 2 + (y - J) ** 2 + z ** 2)

    return r1, r2, r3


class Scratcher(object):
    def __init__(self):
        self.brick = nxt.locator.find_one_brick(name="Stavros")
        self.motors = Motors(
            A=Motor(self.brick, PORT_A),
            B=Motor(self.brick, PORT_B),
            C=Motor(self.brick, PORT_C),
        )
        self.radii = (27, 27, 27)

    def get_new_radii(self, x, y, z):
        """
        Get a point in 3 dimensional space and return the distances that
        the strings have to move in order to go there.
        """
        # Get the absolute radii for the new point.
        r1, r2, r3 = cartesian_to_radii(x, y, z)
        print "New radii:", r1, r2, r3
        # Calculate the deltas from the current point.
        deltas = (r1 - self.radii[0],
                  r2 - self.radii[1],
                  r3 - self.radii[2])
        # Replace the old radii.
        self.radii = (r1, r2, r3)
        return deltas

    def reset(self):
        "Move back to the origin."
        self.move_to(16, 9, 20)

    def turn(self, motor, cm):
        """
        Turn the motor the given distance.

        Turns the motor for the given amount of centimeters. If cm is positive,
        the object is extended, otherwise it is contracted.
        """
        power = 120
        if cm < 0:
            power = -1 * power
            cm = abs(cm)
        motor.turn(power, int(cm * 60))

    def move_to(self, x, y, z):
        print "Moving to", x, y, z
        r1_delta, r2_delta, r3_delta = self.get_new_radii(x, y, z)
        print "Moving by", r1_delta, r2_delta, r3_delta

        threads = (
            Thread(target=self.turn, kwargs={"motor": self.motors.A, "cm": r1_delta}),
            Thread(target=self.turn, kwargs={"motor": self.motors.B, "cm": r2_delta}),
            Thread(target=self.turn, kwargs={"motor": self.motors.C, "cm": r3_delta}),
        )
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]


def main():
    import time
    from random import randint

    scratcher = Scratcher()
    for i in range(10):
        scratcher.move_to(randint(0, 25), randint(0, 25), 20)
        time.sleep(0.5)
    scratcher.reset()


if __name__ == "__main__":
    main()
    #print cartesian_to_radii(0, 0, 5)
