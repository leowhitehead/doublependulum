from __future__ import division
import math as m
import time
import os
import curses

r1 = 11  # line 1 length
r2 = 10  # line 2 length
m1 = 10  # mass of first ball
m2 = 2  # mass of second ball
a1 = m.radians(150)  # Starting angles
a2 = m.radians(70)
a1_v = 0.0  # velocities
a2_v = 0.0
g = 1  # force of gravity

def show(c1, c2):
    global a1
    global a2
    global a1_v
    global a2_v
    global terminal
    maxx = 81
    maxy = 41
    (x1, y1) = c1
    (x2, y2) = c2
    (o1, o2) = (40, 20)
    (x1, y1, x2, y2) = (int(round(x1 + maxx // 2)), 
                        int(round(y1 + maxy// 2)), 
                        int(round(x2 + maxx // 2)),
                        int(round(y2 + maxy // 2)))
    grid = [[' ' for i in range(maxx)] for j in range(maxy)]
    grid[o2][o1] = 'O'
    grid[y1][x1] = 'X'
    if y2 > -1:
        try:
            grid[y2][x2] = 'X'
        except:
            pass
    coords1 = list(bresenham(o1, o2, x1, y1))[1:-1]
    coords2 = list(bresenham(x1, y1, x2, y2))[1:-1]
    for i in coords1:
        grid[i[1]][i[0]] = '*'
    for i in coords2:
        grid[i[1]][i[0]] = '*'
    grid = grid[::-1]
    terminal.addstr(0, 0, '_' * maxx*2)
    for i in range(len(grid)):
        terminal.addstr(i + 1, 0, '|' + ' '.join(grid[i]) + '|') # double spaces each row in grid, fixes scale but looks more choppy
    terminal.addstr(len(grid) + 1, 0, '|' + '_' * (maxx * 2 - 1) + '|')
    terminal.addstr(len(grid) + 3, 0,
                    'P1: ({0: <3}, {1: <3}), P2: ({2: <3}, {3: <3}). a1: {4}, a2: {5}, a1_v: {6: <5}, a2_v: {7: <5} '.format(
        x1 - maxx // 2,
        y1 - maxy // 2,
        x2 - maxx // 2,
        y2 - maxy // 2,
        '{0: <6} d'.format(round(m.degrees(a1), 2) % 360),
        '{0: <6} d'.format(round(m.degrees(a2), 2) % 360),
        round(a1_v, 2),
        round(a2_v, 2),
        ))
    terminal.refresh()

def bresenham(x0, y0, x1, y1):
    '''https://github.com/encukou/bresenham'''
    dx = x1 - x0
    dy = y1 - y0
    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1
    dx = abs(dx)
    dy = abs(dy)
    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0
    D = 2*dy - dx
    y = 0
    for x in range(dx + 1):
        yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy

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
except KeyboardInterrupt:
    curses.endwin()
    exit()
except Exception, e:
    print e
    curses.endwin()
    exit()
