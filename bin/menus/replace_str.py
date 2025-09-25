# Code by Sergio00166

from text_op import search_substring, search_substring_rev
from scr_utils import movcr, hcr, scr, print, movcr
from scr_utils import get_size, str_len
from chg_var_str import chg_var_str
from functions import calc_rel_line
from types import SimpleNamespace
from time import sleep as delay
from upd_scr import update_scr
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
                if menu_state.active:
                    chg_hlg(rel_cursor, menu_state.find_str, app_state)

            if sep != chr(92): setraw(fd, when=TCSADRAIN)


def exit(menu_state):
    global fd, old_settings
    menu_state.run = False
    menu_state.kill = True
    thr.join()
    print(scr)
    if sep != chr(92): tcsetattr(fd, TCSADRAIN, old_settings)


def isin_arr(arr, string):
    for x in arr:
        if string in x:
            return True
    return False


def chg_hlg(rel_cursor, string, app_state):
    pos = rel_cursor - str_len(string)
    mov = movcr % (app_state.line + app_state.banoff, pos + 1)
    if pos >= 0:
        print(mov + app_state.slc + string + app_state.reset + hcr)


def replace(app_state):
    global fd, old_settings, thr
    try:
        find_str = chg_var_str(app_state, "", " [R] Find: ", True)
        if find_str == "":
            raise KeyboardInterrupt
    except KeyboardInterrupt: return
    try:
        replace_str = chg_var_str(app_state, "", " Replace with: ", True)
    except KeyboardInterrupt: return 

    if not isin_arr(app_state.arr, find_str): return

    menu_state = SimpleNamespace(
        find_str=find_str, replace_str=replace_str, active=False, run=False, kill=False
    )
    thr = Thread(target=updscr_thr, args=(app_state, menu_state))
    menu_state.run, menu_state.kill = False, False
    thr.daemon = True
    thr.start()

    pos, menu_state.active = app_state.line + app_state.offset - app_state.banoff, False
    cl_line, app_state.cursor = search_substring(
        app_state.arr, menu_state.find_str, pos, app_state.cursor
    )
    calc_rel_line(app_state, cl_line)
    app_state.cursor -= len(menu_state.find_str)

    while True:
        try:
            if sep != chr(92):
                old = (fd, TCSADRAIN, old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)

            app_state.rows, app_state.columns = get_size()
            rel_cursor = update_scr(app_state, False, menu_state.find_str)

            if menu_state.active:
                chg_hlg(rel_cursor, menu_state.replace_str, app_state)
                menu_state.active = False

            if sep != chr(92): setraw(fd, when=TCSADRAIN)

            menu_state.run = True
            key = getch()
            menu_state.run = False
            pos = app_state.line + app_state.offset - app_state.banoff

            if key == app_state.keys["ctrl+c"] or not isin_arr(
                app_state.arr, menu_state.find_str
            ):  break

            elif key == app_state.keys["arr_right"]:
                cl_line, app_state.cursor = search_substring(
                    app_state.arr, menu_state.find_str, pos, app_state.cursor
                )
                p1 = app_state.arr[cl_line][
                    : app_state.cursor - len(menu_state.find_str)
                ]
                p2 = app_state.arr[cl_line][app_state.cursor :]
                app_state.arr[cl_line] = p1 + menu_state.replace_str + p2
                app_state.cursor = (
                    app_state.cursor
                    + len(menu_state.replace_str)
                    - len(menu_state.find_str)
                )
                calc_rel_line(app_state, cl_line)
                app_state.status_st, menu_state.active = False, True

            elif key == app_state.keys["arr_left"]:
                cl_line, app_state.cursor = search_substring_rev(
                    app_state.arr, menu_state.find_str, pos, app_state.cursor
                )
                p1 = app_state.arr[cl_line][
                    : app_state.cursor - len(menu_state.find_str)
                ]
                p1 = app_state.arr[cl_line][
                    : app_state.cursor - len(menu_state.find_str)
                ]
                p2 = app_state.arr[cl_line][app_state.cursor :]
                app_state.arr[cl_line] = p1 + menu_state.replace_str + p2
                app_state.cursor = (
                    app_state.cursor
                    + len(menu_state.replace_str)
                    - len(menu_state.find_str)
                )
                calc_rel_line(app_state, cl_line)
                app_state.status_st, menu_state.active = False, True

            elif key == app_state.keys["ctrl+a"]:
                for p, x in enumerate(app_state.arr):
                    app_state.arr[p] = x.replace(
                        menu_state.find_str, menu_state.replace_str
                    )
                app_state.status_st = False
                break

        except: pass

    exit(menu_state)

 