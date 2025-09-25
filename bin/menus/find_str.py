# Code by Sergio00166

from text_op import search_substring, search_substring_rev
from scr_utils import get_size, str_len, movcr
from scr_utils import hcr, scr, print
from upd_scr import update_scr
from chg_var_str import chg_var_str
from functions import calc_rel_line
from types import SimpleNamespace
from time import sleep as delay
from threading import Thread
from inputs import getch
from os import sep


if sep != chr(92):
    from termios import TCSADRAIN, tcsetattr, tcgetattr
    from sys import stdin
    from tty import setraw

    fd = stdin.fileno()
    old_settings = tcgetattr(fd)


def updscr_thr(app_state, menu_state):
    global fd, old_settings

    while not menu_state.kill:
        delay(0.01)
        if menu_state.run:
            if sep != chr(92):
                old = (fd, TCSADRAIN, old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)

            old_rows = app_state.rows
            old_columns = app_state.columns
            app_state.rows, app_state.columns = get_size()

            if app_state.rows < 4 or app_state.columns < 24:
                print("\r\033cTerminal too small")

            elif not (old_rows == app_state.rows and old_columns == app_state.columns):
                if app_state.line > app_state.rows:
                    app_state.offset = app_state.offset + (
                        app_state.line - app_state.rows
                    )
                    app_state.line = app_state.rows

                if sep != chr(92): tcsetattr(fd, TCSADRAIN, old_settings)
                rel_cursor = update_scr(app_state, False, menu_state.find_str)
                chg_hlg(rel_cursor, menu_state.find_str, app_state)

            if sep != chr(92): setraw(fd, when=TCSADRAIN)


def exit(menu_state):
    global fd, old_settings
    menu_state.run = False
    menu_state.kill = True
    thr.join()
    print(scr)
    if sep != chr(92): tcsetattr(fd, TCSADRAIN, old_settings)


def chg_hlg(rel_cursor, find_str, app_state):
    pos = rel_cursor - str_len(find_str)
    mov = movcr % (app_state.line + app_state.banoff, pos + 1)
    if pos >= 0:
        print(mov + app_state.slc + find_str + app_state.reset + hcr)


def isin_arr(arr, string):
    for x in arr:
        if string in x: 
            return True
    return False


def find(app_state):
    global fd, old_settings, thr

    try: find_str = chg_var_str(app_state, "", " Find: ", True)
    except KeyboardInterrupt: return

    if not isin_arr(app_state.arr, find_str) or find_str == "": return
    menu_state = SimpleNamespace(find_str=find_str, run=False, kill=False)

    thr = Thread(target=updscr_thr, args=(app_state, menu_state))
    menu_state.run, menu_state.kill = False, False
    thr.daemon = True
    thr.start()

    pos = app_state.line + app_state.offset - app_state.banoff
    p1, app_state.cursor = search_substring(
        app_state.arr, menu_state.find_str, pos, app_state.cursor
    )
    calc_rel_line(app_state, p1)

    while True:
        try:
            if sep != chr(92):
                old = (fd, TCSADRAIN, old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)

            app_state.rows, app_state.columns = get_size()
            rel_cursor = update_scr(app_state, False, menu_state.find_str)

            chg_hlg(rel_cursor, menu_state.find_str, app_state)
            if sep != chr(92): setraw(fd, when=TCSADRAIN)
            pos = app_state.line + app_state.offset - app_state.banoff

            menu_state.run = True
            key = getch()
            menu_state.run = False

            if key == app_state.keys["ctrl+c"]: break

            elif key == app_state.keys["arr_right"]:
                p1, app_state.cursor = search_substring(
                    app_state.arr, menu_state.find_str, pos, app_state.cursor
                )
                calc_rel_line(app_state, p1)

            elif key == app_state.keys["arr_left"]:
                p1, app_state.cursor = search_substring_rev(
                    app_state.arr, menu_state.find_str, pos, app_state.cursor
                )
                calc_rel_line(app_state, p1)

        except: pass
    exit(menu_state)

 