Back scratcher
==============

Back scratcher is a LEGO Mindstorms robot that can address any point in 3D
space below and within it. Here's what it looks like:

![The back scratcher](http://media.korokithakis.net/images/robot/robot.jpg)

That's just the prototype, you can make yours as large as you need. The servos
don't need to be at the edges (and shouldn't, they're pretty heavy). A very
effective alternate configuration would have the servos in some configuration
above the arms and spool the string to the edges.

This repository contains the software to run this robot. You can either use the
nxt-python version (`scratcher.py`), or the NXC version (`scratcher.nxc`). The
nxt-python version is easier to hack, but the NXC version can be compiled and
sent to the brick so it works offline, for those extra-long back scratching
sessions.

All you need to do is set D to the length of each side of the triangle, and CM
to the number of degrees per centimeter of servo motion. The rest should just
work!
