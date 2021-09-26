import time
import curses


def draw(canvas):
    convas1 = curses.newwin(40,20,2,2)
    convas2 = curses.newwin(10,10,10,40)
    convas1.border()
    convas2.border()
    row, column = (1, 1)
    convas1.addstr(row, column, 'Hello, World!')
    convas1.refresh()
    convas2.refresh()
    time.sleep(10)
  
if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)