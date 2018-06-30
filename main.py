from __future__ import division
import math as m
import time
import os
import curses

r1 = 11
r2 = 10
m1 = 10
m2 = 10
m2 = 2
a1 = m.radians(120)
a2 = m.radians(70)
a1_v = 0.0
a2_v = 0.0
g = 1

def show(c1, c2):
    global a1
    global a2
    global a1_v
    global a2_v
    global terminal
    (x1, y1) = c1
    (x2, y2) = c2
    (o1, o2) = (60, 30)
    (x1, y1, x2, y2) = (int(round(x1 + 60)), int(round(y1 + 30)),
                        int(round(x2 + 60)), int(round(y2 + 30)))
    grid = [[' ' for i in range(121)] for j in range(61)]
    grid[o2][o1] = 'O'
    grid[y1][x1] = 'X'
    grid[y2][x2] = 'x'
    grid = grid[::-1]
    for i in range(len(grid)):
        terminal.addstr(i, 0, ''.join(grid[i]))
    terminal.addstr(len(grid) + 1, 0,
                    'P1: ({}, {}), P2: ({}, {}). a1: {}, a2: {}, a1_v: {}, a2_v: {}         '.format(
        x1 - 60,
        y1 - 30,
        x2 - 60,
        y2 - 30,
        "{} d".format(round(m.degrees(a1), 2)),
        "{} d".format(round(m.degrees(a2), 2)),
        round(a1_v, 2),
        round(a2_v, 2),
        ))
    terminal.refresh()


terminal = curses.initscr()
curses.noecho()
curses.cbreak()
terminal.nodelay(1)
try:
    while True:
        time.sleep(0.1)
        x1 = r1 * m.sin(a1)
        y1 = -r1 * m.cos(a1)
        x2 = x1 + r2 * m.sin(a2)
        y2 = y1 - r2 * m.cos(a2)
        show((x1, y1), (x2, y2))

        num1 = -g * (2 * m1 + m2) * m.sin(a1)
        num2 = -m2 * g * m.sin(a1 - 2 * a2)
        num3 = -2 * m.sin(a1 - a2) * m2
        num4 = a2_v * a2_v * r2 + a1_v * a1_v * r1 * m.cos(a1 - a2)
        den = r1 * (2 * m1 + m2 - m2 * m.cos(2 * a1 - 2 * a2))
        a1_a = (num1 + num2 + num3 * num4) / den

        num1 = 2 * m.sin(a1 - a2)
        num2 = a1_v * a1_v * r1 * (m1 + m2)
        num3 = g * (m1 + m2) * m.cos(a1)
        num4 = a2_v * a2_v * r2 * m2 * m.cos(a1 - a2)
        den = r2 * (2 * m1 + m2 - m2 * m.cos(2 * a1 - 2 * a2))
        a2_a = num1 * (num2 + num3 + num4) / den

        a1_v += a1_a
        a2_v += a2_a
        a1 += a1_v
        a2 += a2_v
except Exception, e:
    print e
    curses.endwin()
    exit()