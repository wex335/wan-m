import json,curses

print("hello")
converstations = []

def main(window:curses.window):
    while True:
        window.clear
        key = str(window.get_wch())
        window.addstr(1,1,f'key {key}                ')
        window.addstr(2,1,f'len {len(key)}            ')
        window.addstr(3,1,f'ord {ord(key)}             ')
        window.addstr(4,1,f'chr {chr(ord(key))}             ')
        window.refresh()


curses.update_lines_cols()
curses.wrapper(main)