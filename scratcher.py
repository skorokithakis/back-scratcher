#!./env/bin/python

import math
import nxt.locator
import time

from nxt.motor import PORT_A, PORT_B, PORT_C
from nxt.motcont import MotCont
from collections import namedtuple

# The wheel has a circumference of 6 cm averaged over 10 turns.
# The diameter of 1.9 agrees with the result.
# 1 cm = 60 degrees
CM = 60.0

# From http://en.wikipedia.org/wiki/Trilateration
# Motor A is 0, 0, 0
# Motor B is 0, D, 0
# Motor C is I, J, 0
D = 32.0
I = D / 2
J = 0.86 * D


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
        self.motcont = MotCont(self.brick)
        self.motcont.start()
        self.power = 60
        self.initial_radii = (30, 30, 30)

    def move_to_radii(self, r1, r2, r3):
        "Move to the given radii, relative to the starting position."

        # These are absolute radii, thanks to motcont.
        radii = (r1, r2, r3)

        # Sanity checks.
        radii = [max(radius, 5) for radius in radii]

        # Subtract the new position from the initial position. Since the software
        # doesn't know we're at some point (x, y, z) to begin with, it treats the
        # starting position as (0, 0, 0). The calculation here compensates for that.
        radii = [(radius - initial) for radius, initial in zip(radii, self.initial_radii)]

        # Convert the given radii from cm to degrees.
        degrees = [radius * CM for radius in radii]
        ports = (PORT_A, PORT_B, PORT_C)

        for port, degrees in zip(ports, degrees):
            self.motcont.move_to(port, self.power, int(degrees), smoothstart=1, brake=1)

        while not all(self.motcont.is_ready(port) for port in ports):
            time.sleep(0.1)

    def reset(self):
        "Move back to the origin."
        self.move_to_radii(*self.initial_radii)

    def move_to(self, x, y, z):
        print "Moving to", x, y, z
        r1, r2, r3 = cartesian_to_radii(x, y, z)
        print "Moving to radii", r1, r2, r3
        self.move_to_radii(r1, r2, r3)


def main():
    from random import randint

    scratcher = Scratcher()
    for i in range(5):
        scratcher.move_to(randint(0, 25), randint(0, 25), randint(5, 25))
    scratcher.move_to(0, 0, 30)
    scratcher.reset()


if __name__ == "__main__":
    #main()
    print radii_to_cartesian(29, 29, 29)
