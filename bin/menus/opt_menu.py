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


if not sep == chr(92):  # If OS is LINUX
    # Get default values for TTY
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
            # If OS is LINUX restore TTY to it default values
            if not sep == chr(92):
                old = (fd, TCSADRAIN, old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            mode = (menu_state.text, "", menu_state.wrtptr, 0)
            menu_updsrc(app_state, mode)
            print(hcr)  # Hide the cursor
            # If OS is LINUX set TTY to raw mode
            if not sep == chr(92):
                setraw(fd, when=TCSADRAIN)


def exit(menu_state):
    global fd, old_settings, thr
    menu_state.run = False
    menu_state.kill = True
    thr.join()
    print(scr)  # Show cursor again
    if not sep == chr(92):
        tcsetattr(fd, TCSADRAIN, old_settings)


def opt_menu(app_state):
    global fd, old_settings, thr

    # Create menu state object
    menu_state = SimpleNamespace(text="", wrtptr=1, run=False, kill=False)

    menu_state.text = "S (CharSet), L (LineSep), "
    menu_state.text += "TAB (Tab/Sp), C (Chg cmnt), "
    menu_state.text += "E (Chg end cmnt), I (Chg indent)"
    menu_state.text, menu_state.wrtptr = " Options: " + menu_state.text, 1

    thr = Thread(target=updscr_thr, args=(app_state, menu_state))
    menu_state.run, menu_state.kill = False, False
    thr.daemon = True
    thr.start()
    print(hcr)  # Hide the cursor

    while True:
        # Fix when the cursor is out
        if len(menu_state.text) < menu_state.wrtptr:
            menu_state.wrtptr = len(menu_state.text)
        try:
            # Force use LINUX dir separator
            menu_state.text = menu_state.text.replace(chr(92), "/")
            # If OS is LINUX restore TTY to it default values
            if not sep == chr(92):
                old = (fd, TCSADRAIN, old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            mode = (menu_state.text, "", menu_state.wrtptr, 0)
            menu_updsrc(app_state, mode, True)
            print(hcr)  # Hide the cursor
            # If OS is LINUX set TTY to raw mode
            if not sep == chr(92):
                setraw(fd, when=TCSADRAIN)

            menu_state.run = True  # Start update screen thread
            key = getch()  # Map keys
            menu_state.run = False  # Stop update screen thread

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

    exit(menu_state)  # Reset

