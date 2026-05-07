# Code by Sergio00166

from upd_scr import menu_updsrc, hcr, scr, print
from chg_var_str import chg_var_str
from codec_menu import codec_menu
from lnsep_menu import lnsep_menu
from types import SimpleNamespace
from time import sleep as delay
from scr_utils import get_size
from threading import Thread
from inputs import getch
from data import keys
from os import sep

menu_text = "S (CharSet), L (LineSep), TAB (Tab/Sp), C (Chg cmnt), E (Chg end cmnt), I (Chg indent) "

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


def opt_menu(app_state):
    global fd, old_settings

    menu_state = SimpleNamespace(
        text = f" Options: {menu_text}",
        wrtptr = 1, run = False, kill = False
    )
    thr = Thread(target=updscr_thr, args=(app_state, menu_state))
    menu_state.run, menu_state.kill = False, False
    thr.daemon = True; thr.start(); print(hcr)

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
            kbd_input = getch()
            menu_state.run = False

            menu_actions(app_state, menu_state, kbd_input)

        except KeyboardInterrupt: break
        except: pass

    menu_state.run, menu_state.kill = False, True
    thr.join(); print(scr) # Wait and show cursor
    if sep != chr(92): tcsetattr(fd, TCSADRAIN, old_settings)


def menu_actions(app_state, menu_state, kbd_input):

    if kbd_input == keys["ctrl+c"]: raise KeyboardInterrupt

    elif kbd_input == b"\t":
        app_state.indent = " " * 4 if app_state.indent == "\t" else "\t"

    elif kbd_input == keys["arr_left"]:
        menu_state.wrtptr -= app_state.columns
        menu_state.wrtptr = max(menu_state.wrtptr, 1)

    elif kbd_input == keys["arr_right"]:
        menu_state.wrtptr += app_state.columns + 2
        menu_state.wrtptr = min(menu_state.wrtptr, len(menu_state.text))

    elif kbd_input == b"c":
        try:
            args = (app_state, app_state.comment[0], " Set comment: ")
            app_state.comment[0] = chg_var_str(*args)
        except KeyboardInterrupt: return
        raise  KeyboardInterrupt

    elif kbd_input == b"e":
        try:
            args = (app_state, app_state.comment[1], " Set end cmt: ")
            app_state.comment[1] = chg_var_str(*args)
        except KeyboardInterrupt: return
        raise  KeyboardInterrupt

    elif kbd_input == b"i":
        try:
            args = (app_state, app_state.comment[1], " Set indent: ")
            app_state.indent = chg_var_str(*args)
        except KeyboardInterrupt: return
        raise  KeyboardInterrupt

    elif kbd_input == b"s":
        try: codec_menu(app_state)
        except KeyboardInterrupt: return
        raise  KeyboardInterrupt

    elif kbd_input == b"l":
        try: lnsep_menu(app_state)
        except KeyboardInterrupt: return
        raise  KeyboardInterrupt


 