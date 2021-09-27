from iop import *
from consoleManager import Console
from lp import *
from internet import *
import curses,json,sys,os



def main(win:curses.window):
    try:
        while True:
            k = win.getch()
            if k == 6:
                log('@$%^&U(OPOIUYTR^&*(IJHBGV))')
            log(f"key {k} {curses.keyname(k)}")
            win.addstr(1,1,k.__str__())
            win.refresh
    except Exception as d:
        log(d)

curses.update_lines_cols()
curses.wrapper(main)