# Code by Sergio00166

from upd_scr import menu_updsrc
from scr_utils import hcr, scr, print
from types import SimpleNamespace
from chg_var_str import chg_var_str
from time import sleep as delay
from scr_utils import get_size
from threading import Thread
from inputs import getch
from os import sep

menu_text = "1 (ASCII), 2 (UTF8), 3 (UTF8-BOM), 4 (UTF16), 5 (UTF16-BE), 6 (UTF16-LE) "


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

            mode = (menu_state.text, "", menu_state.wrtptr, 0)
            menu_updsrc(app_state, mode)
            print(hcr)
            if sep != chr(92): setraw(fd, when=TCSADRAIN)


def exit(menu_state):
    global fd, old_settings, thr
    menu_state.run = False
    menu_state.kill = True
    thr.join()
    print(scr)
    if sep != chr(92): tcsetattr(fd, TCSADRAIN, old_settings)


def codec_menu(app_state):
    global fd, old_settings, thr

    menu_state = SimpleNamespace(text="", wrtptr=1, run=False, kill=False)
    app_state.status_st = True    
    app_state.status = "ASCII" if app_state.codec == "latin_1" else app_state.codec
    menu_state.text = f" Codec: {menu_text}"
    menu_state.wrtptr = 1

    thr = Thread(target=updscr_thr, args=(app_state, menu_state))
    menu_state.run, menu_state.kill = False, False
    thr.daemon = True
    thr.start()
    print(hcr)

    while True:
        if len(menu_state.text) < menu_state.wrtptr:
            menu_state.wrtptr = len(menu_state.text)
        try:
            menu_state.text = menu_state.text.replace(chr(92), "/")
            if sep != chr(92):
                old = (fd, TCSADRAIN, old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)

            mode = (menu_state.text, "", menu_state.wrtptr, 0)
            menu_updsrc(app_state, mode, True)
            print(hcr)
            if sep != chr(92): setraw(fd, when=TCSADRAIN)

            menu_state.run = True
            key = getch()
            menu_state.run = False

            if key == app_state.keys["ctrl+c"]:              break
            elif key == b"1": app_state.codec = "latin_1";   break
            elif key == b"2": app_state.codec = "utf-8";     break
            elif key == b"3": app_state.codec = "utf-8-sig"; break
            elif key == b"4": app_state.codec = "utf-16";    break
            elif key == b"5": app_state.codec = "utf-16-be"; break
            elif key == b"6": app_state.codec = "utf-16-le"; break

            elif key == app_state.keys["arr_left"]:
                menu_state.wrtptr -= app_state.columns
                menu_state.wrtptr = max(menu_state.wrtptr, 1)

            elif key == app_state.keys["arr_right"]:
                menu_state.wrtptr += app_state.columns + 2
                menu_state.wrtptr = min(menu_state.wrtptr, len(menu_state.text))

        except: pass

    app_state.status_st = False
    exit(menu_state)

 