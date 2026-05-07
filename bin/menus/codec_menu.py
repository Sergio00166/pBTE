# Code by Sergio00166

from upd_scr import menu_updsrc
from scr_utils import hcr, scr, print
from types import SimpleNamespace
from chg_var_str import chg_var_str
from time import sleep as delay
from scr_utils import get_size
from threading import Thread
from inputs import getch
from data import keys
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
        if not menu_state.run: continue

        if sep != chr(92):
            old = (fd, TCSADRAIN, old_settings)
            tcsetattr(fd, TCSADRAIN, old_settings)

        mode = (menu_state.text, "", menu_state.wrtptr, 0)
        menu_updsrc(app_state, mode); print(hcr)
        if sep != chr(92): setraw(fd, when=TCSADRAIN)


def codec_menu(app_state):
    global fd, old_settings

    menu_state = SimpleNamespace(
        text = f" Codec: {menu_text}",
        wrtptr = 1, run = False, kill = False
    )
    app_state.status = "ASCII" if app_state.codec == "latin_1" else app_state.codec
    app_state.status_st = True 

    thr = Thread(target=updscr_thr, args=(app_state, menu_state))
    menu_state.run, menu_state.kill = False, False
    thr.daemon = True; thr.start(); print(hcr)
    exit_w_raise = False

    while True:
        if len(menu_state.text) < menu_state.wrtptr:
            menu_state.wrtptr = len(menu_state.text)
        try:
            menu_state.text = menu_state.text.replace(chr(92), "/")
            if sep != chr(92):
                old = (fd, TCSADRAIN, old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)

            mode = (menu_state.text, "", menu_state.wrtptr, 0)
            menu_updsrc(app_state, mode, True); print(hcr)
            if sep != chr(92): setraw(fd, when=TCSADRAIN)

            menu_state.run = True
            kbd_input = getch()
            menu_state.run = False

            if kbd_input == keys["ctrl+c"]: exit_w_raise = True;   break
            elif kbd_input == b"1": app_state.codec = "latin_1";   break
            elif kbd_input == b"2": app_state.codec = "utf-8";     break
            elif kbd_input == b"3": app_state.codec = "utf-8-sig"; break
            elif kbd_input == b"4": app_state.codec = "utf-16";    break
            elif kbd_input == b"5": app_state.codec = "utf-16-be"; break
            elif kbd_input == b"6": app_state.codec = "utf-16-le"; break

            elif kbd_input == keys["arr_left"]:
                menu_state.wrtptr -= app_state.columns
                menu_state.wrtptr = max(menu_state.wrtptr, 1)

            elif kbd_input == keys["arr_right"]:
                menu_state.wrtptr += app_state.columns + 2
                menu_state.wrtptr = min(menu_state.wrtptr, len(menu_state.text))

        except: pass

    app_state.status_st = False
    menu_state.run, menu_state.kill = False, True
    thr.join(); print(scr) # Wait and show cursor
    if sep != chr(92): tcsetattr(fd, TCSADRAIN, old_settings)
    if exit_w_raise: raise KeyboardInterrupt


 