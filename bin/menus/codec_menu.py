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


def codec_menu(app_state):
    global fd, old_settings, thr

    # Create menu state object
    menu_state = SimpleNamespace(text="", wrtptr=1, run=False, kill=False)

    app_state.status_st = True
    app_state.status = "ASCII" if app_state.codec == "latin_1" else app_state.codec
    menu_state.text = "1 (ASCII), 2 (UTF8), "
    menu_state.text += "3 (UTF8-BOM), 4 (UTF16), "
    menu_state.text += "5 (UTF16-BE), 6 (UTF16-LE) "
    menu_state.text, menu_state.wrtptr = f" Codec: " + menu_state.text, 1

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

    # Reset and hide status
    app_state.status_st = False
    exit(menu_state)

