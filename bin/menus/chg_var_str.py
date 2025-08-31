# Code by Sergio00166

from types import SimpleNamespace
from inputs import decode, getch
from upd_scr import menu_updsrc
from time import sleep as delay
from scr_utils import get_size
from threading import Thread
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
            mode = (
                menu_state.entered_str,
                menu_state.prt_txt,
                menu_state.wrtptr,
                menu_state.lenght,
            )
            menu_updsrc(app_state, mode)
            # If OS is LINUX set TTY to raw mode
            if not sep == chr(92):
                setraw(fd, when=TCSADRAIN)


def exit(menu_state):
    global fd, old_settings
    menu_state.run = False
    menu_state.kill = True
    thr.join()
    if not sep == chr(92):
        tcsetattr(fd, TCSADRAIN, old_settings)


def chg_var_str(app_state, entered_str, prt_txt, kctlc_f=False):
    global fd, old_settings, thr

    # Create menu state object
    menu_state = SimpleNamespace(
        entered_str=entered_str,
        prt_txt=prt_txt,
        lenght=len(prt_txt) + 1,
        wrtptr=len(prt_txt) + 1 + len(entered_str),
        kctlc=False,
        run=False,
        kill=False,
    )

    old_str = menu_state.entered_str
    thr = Thread(target=updscr_thr, args=(app_state, menu_state))
    menu_state.run, menu_state.kill, menu_state.kctlc = False, False, False
    thr.daemon = True
    thr.start()

    while True:
        # Fix when the cursor is out
        if len(menu_state.entered_str) < menu_state.wrtptr - menu_state.lenght:
            menu_state.wrtptr = len(menu_state.entered_str) + menu_state.lenght
        try:
            # If OS is LINUX restore TTY to it default values
            if not sep == chr(92):
                old = (fd, TCSADRAIN, old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            mode = (
                menu_state.entered_str,
                menu_state.prt_txt,
                menu_state.wrtptr,
                menu_state.lenght,
            )
            menu_updsrc(app_state, mode, True)
            # If OS is LINUX set TTY to raw mode
            if not sep == chr(92):
                setraw(fd, when=TCSADRAIN)

            menu_state.run = True  # Start update screen thread
            key = getch()  # Map keys
            menu_state.run = False  # Stop update screen thread

            if key == app_state.keys["return"]: break

            elif key == app_state.keys["ctrl+c"]:
                menu_state.entered_str = old_str
                if kctlc_f:
                    menu_state.kctlc = True
                break

            elif key == app_state.keys["delete"]:
                if not menu_state.wrtptr == menu_state.lenght:
                    p1 = list(menu_state.entered_str)
                    p1.pop(menu_state.wrtptr - menu_state.lenght - 1)
                    menu_state.entered_str = "".join(p1)
                    menu_state.wrtptr -= 1

            elif key == app_state.keys["arr_left"]:
                if not menu_state.wrtptr == menu_state.lenght:
                    menu_state.wrtptr -= 1

            elif key == app_state.keys["arr_right"]:
                if (
                    not menu_state.wrtptr
                    > len(menu_state.entered_str) + menu_state.lenght
                ):
                    menu_state.wrtptr += 1

            elif key == app_state.keys["supr"]:
                p1 = list(menu_state.entered_str)
                p1.pop(menu_state.wrtptr - menu_state.lenght)
                menu_state.entered_str = "".join(p1)

            elif key in app_state.keys["start"]:
                menu_state.wrtptr = menu_state.lenght

            elif key in app_state.keys["end"]:
                menu_state.wrtptr = len(menu_state.entered_str) + menu_state.lenght

            else:  # Rest of keys
                if menu_state.wrtptr < ((app_state.columns + 2) * app_state.rows + 1):
                    out = decode(key)
                    p1 = menu_state.entered_str[: menu_state.wrtptr - menu_state.lenght]
                    p2 = menu_state.entered_str[menu_state.wrtptr - menu_state.lenght :]
                    menu_state.entered_str = p1 + out + p2
                    menu_state.wrtptr += len(out)
                    complete = False
        except: pass

    exit(menu_state)  # Reset
    if menu_state.kctlc:
        raise KeyboardInterrupt
    return menu_state.entered_str

