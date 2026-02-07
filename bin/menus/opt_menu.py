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
from os import sep

menu_text = "S (CharSet), L (LineSep),TAB (Tab/Sp), C (Chg cmnt), E (Chg end cmnt), I (Chg indent) "


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


def opt_menu(app_state):
    global fd, old_settings, thr

    menu_state = SimpleNamespace(text="", wrtptr=1, run=False, kill=False)
    menu_state.text = f" Options: {menu_text}"
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

            if key == app_state.keys["ctrl+c"]: break

            elif key == b"\t":
                app_state.indent = " " * 4 if app_state.indent == "\t" else "\t"
                break

            elif key == b"c":
                app_state.comment[0] = chg_var_str(
                    app_state, app_state.comment[0], " Set comment: "
                )
                break

            elif key == b"e":
                app_state.comment[1] = chg_var_str(
                    app_state, app_state.comment[1], " Set end cmt: "
                )
                break

            elif key == b"i":
                app_state.indent = chg_var_str(
                    app_state, app_state.indent, " Set indent: "
                )
                break

            elif key == b"s": codec_menu(app_state); break
            elif key == b"l": lnsep_menu(app_state); break

            elif key == app_state.keys["arr_left"]:
                menu_state.wrtptr -= app_state.columns
                menu_state.wrtptr = max(menu_state.wrtptr, 1)

            elif key == app_state.keys["arr_right"]:
                menu_state.wrtptr += app_state.columns + 2
                menu_state.wrtptr = min(menu_state.wrtptr, len(menu_state.text))

        except: pass

    exit(menu_state)

 