# Code by Sergio00166

from types import SimpleNamespace
from inputs import decode, getch
from upd_scr import menu_updsrc
from time import sleep as delay
from data import keys, keys_raw
from scr_utils import get_size
from threading import Thread
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
        if not menu_state.run: continue

        if sep != chr(92):
            old = (fd, TCSADRAIN, old_settings)
            tcsetattr(fd, TCSADRAIN, old_settings)

        mode = (
            menu_state.entered_str,
            menu_state.prt_txt,
            menu_state.wrtptr,
            menu_state.lenght,
        )
        menu_updsrc(app_state, mode)

        if sep != chr(92): setraw(fd, when=TCSADRAIN)


def chg_var_str(app_state, entered_str, prt_txt):
    global fd, old_settings

    menu_state = SimpleNamespace(
        entered_str = entered_str,
        lenght = len(prt_txt) + 1,
        wrtptr = len(prt_txt) + 1 + len(entered_str),
        prt_txt = prt_txt,
        run = False,
        kill = False
    )
    thr = Thread(target=updscr_thr, args=(app_state, menu_state))
    thr.daemon = True; thr.start()
    exit_w_raise = False

    while True:
        if len(menu_state.entered_str) < menu_state.wrtptr - menu_state.lenght:
            menu_state.wrtptr = len(menu_state.entered_str) + menu_state.lenght
        try:
            if sep != chr(92):
                old = (fd, TCSADRAIN, old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)

            mode = (
                menu_state.entered_str,
                menu_state.prt_txt,
                menu_state.wrtptr,
                menu_state.lenght,
            )
            menu_updsrc(app_state, mode, True)
            if sep != chr(92): setraw(fd, when=TCSADRAIN)

            menu_state.run = True
            kbd_input = getch()
            menu_state.run = False

            if kbd_input == keys["ctrl+c"]:
                menu_state.entered_str = entered_str
                exit_w_raise = True; break
                
            if kbd_input == keys["return"]: break
            menu_actions(app_state, menu_state, kbd_input)

        except: pass

    menu_state.run = False
    menu_state.kill = True
    thr.join() # Wait for update thread to finish
    if sep != chr(92): tcsetattr(fd, TCSADRAIN, old_settings)
    if exit_w_raise: raise KeyboardInterrupt
    return menu_state.entered_str


def menu_actions(app_state, menu_state, kbd_input):

    if kbd_input in keys["start"]:
        menu_state.wrtptr = menu_state.lenght

    elif kbd_input in keys["end"]:
        menu_state.wrtptr = len(menu_state.entered_str) + menu_state.lenght


    elif kbd_input == keys["arr_left"]:
        if not menu_state.wrtptr == menu_state.lenght:
            menu_state.wrtptr -= 1

    elif kbd_input == keys["arr_right"]:
        total = len(menu_state.entered_str) + menu_state.lenght
        if not menu_state.wrtptr > total: menu_state.wrtptr += 1


    elif kbd_input == keys["delete"]:
        idx = menu_state.wrtptr - menu_state.lenght
        if idx >= len(menu_state.entered_str): return
        p1 = list(menu_state.entered_str)
        p1.pop(idx) # Remove last char
        menu_state.entered_str = "".join(p1)


    elif kbd_input == keys["backspace"]:
        if menu_state.wrtptr == menu_state.lenght: return
        p1 = list(menu_state.entered_str)
        p1.pop(menu_state.wrtptr - menu_state.lenght - 1)
        menu_state.entered_str = "".join(p1)
        menu_state.wrtptr -= 1


    elif kbd_input in keys_raw: pass

    elif menu_state.wrtptr < ((app_state.columns + 2) * app_state.rows + 1):
        out = decode(kbd_input)
        p1 = menu_state.entered_str[: menu_state.wrtptr - menu_state.lenght]
        p2 = menu_state.entered_str[menu_state.wrtptr - menu_state.lenght :]
        menu_state.entered_str = p1 + out + p2
        menu_state.wrtptr += len(out)
        complete = False


 