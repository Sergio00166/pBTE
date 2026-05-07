# Code by Sergio00166

from functions import write_UTF8
from types import SimpleNamespace
from inputs import decode, getch
from data import keys, keys_raw
from upd_scr import menu_updsrc
from time import sleep as delay
from scr_utils import get_size
from threading import Thread
from glob import glob
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
            menu_state.filewrite,
            menu_state.saveastxt,
            menu_state.wrtptr,
            menu_state.lenght
        )
        menu_updsrc(app_state, mode)
        if sep != chr(92): setraw(fd, when=TCSADRAIN)


def save_as(app_state):
    global fd, old_settings

    menu_state = SimpleNamespace(
        saveastxt = " Save as: ",
        filewrite = app_state.filename,
        auto_complete = False,
        lenght = 0,
        wrtptr = 0,
        content = [],
        cmp_counter = 0,
        run = False,
        kill = False
    )
    menu_state.lenght = len(menu_state.saveastxt) + 1
    menu_state.wrtptr = menu_state.lenght + len(menu_state.filewrite)

    thr = Thread(target=updscr_thr, args=(app_state, menu_state))
    thr.daemon = True; thr.start()

    while True:
        if len(menu_state.filewrite) < menu_state.wrtptr  - menu_state.lenght:
            menu_state.wrtptr = len(menu_state.filewrite) + menu_state.lenght
        try:
            menu_state.filewrite = menu_state.filewrite.replace(chr(92), "/")
            if sep != chr(92):
                old = (fd, TCSADRAIN, old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)

            mode = (
                menu_state.filewrite,
                menu_state.saveastxt,
                menu_state.wrtptr,
                menu_state.lenght,
            )
            menu_updsrc(app_state, mode, True)
            if sep != chr(92): setraw(fd, when=TCSADRAIN)

            menu_state.run = True
            kbd_input = getch()
            menu_state.run = False

            if app_state.status == "ERROR":
                app_state.status_st = False

            menu_actions(app_state, menu_state, kbd_input)

        except KeyboardInterrupt: break
        except OSError:
            app_state.status = "ERROR"
            app_state.status_st = True
        except: pass

    menu_state.run, menu_state.kill = False, True
    thr.join() # Wait for update thread to finish
    if sep != chr(92): tcsetattr(fd, TCSADRAIN, old_settings)


def menu_actions(app_state, menu_state, kbd_input):

    if menu_state.auto_complete and kbd_input == keys["return"]:
        menu_state.wrtptr = len(menu_state.filewrite + menu_state.saveastxt) + 2
        menu_state.auto_complete = False

    elif kbd_input == keys["arr_left"]:
        if not menu_state.wrtptr == menu_state.lenght:
            menu_state.wrtptr -= 1

    elif kbd_input == keys["arr_right"]:
        total = len(menu_state.filewrite) + menu_state.lenght
        if not menu_state.wrtptr > total: menu_state.wrtptr += 1

    elif kbd_input == keys["tab"]:
        if (len(menu_state.filewrite) == 0 or
           (sep == chr(92) and not ":/" in menu_state.filewrite)
        ): return
        
        if not menu_state.auto_complete:
            menu_state.content = glob(menu_state.filewrite + "*", recursive=False)

        if len(menu_state.content) > 0: menu_state.auto_complete = True

        if menu_state.cmp_counter >= len(menu_state.content):
            menu_state.cmp_counter = 0

        if menu_state.auto_complete:
            menu_state.filewrite = menu_state.content[menu_state.cmp_counter]
            menu_state.cmp_counter += 1


    elif kbd_input in (keys["ctrl+s"], keys["ctrl+b"]):
        suffix = ".bak" if kbd_input == keys["ctrl+b"] else ""
        save_file = menu_state.filewrite + suffix
        try:
            write_UTF8(app_state, save_file)

            if kbd_input == keys["ctrl+b"]:
                app_state.status = "BCKPd"
            else:
                app_state.status = "SAVED"
                app_state.filename = menu_state.filewrite

            app_state.status_st = True
            raise KeyboardInterrupt
        except:
            app_state.status, app_state.status_st = "ERROR", True


    elif kbd_input == keys["backspace"]:
        if not menu_state.wrtptr == menu_state.lenght:

            if menu_state.auto_complete:
                menu_state.filewrite = menu_state.filewrite.split("/")[:-1]
                menu_state.filewrite = "/".join(menu_state.filewrite) + "/"
                menu_state.wrtptr -= len(menu_state.filewrite[-1]) - 1
                menu_state.auto_complete = False
            else:
                p1 = list(menu_state.filewrite)
                p1.pop(menu_state.wrtptr - menu_state.lenght - 1)
                menu_state.filewrite = "".join(p1)
                menu_state.wrtptr -= 1


    elif kbd_input == keys["delete"]:
        if menu_state.auto_complete:
            menu_state.filewrite = menu_state.filewrite.split("/")[:-1]
            menu_state.filewrite = "/".join(menu_state.filewrite) + "/"
            menu_state.wrtptr -= len(menu_state.filewrite[-1]) - 1
            menu_state.auto_complete = False
        else:
            idx = menu_state.wrtptr - menu_state.lenght
            if idx >= len(menu_state.filewrite): return
            p1 = list(menu_state.filewrite)
            p1.pop(idx) # Remove last char
            menu_state.filewrite = "".join(p1)


    elif kbd_input in keys["start"]:
        menu_state.wrtptr = menu_state.lenght

    elif kbd_input in keys["end"]:
        menu_state.wrtptr = len(menu_state.filewrite) + menu_state.lenght

    elif kbd_input == keys["ctrl+c"]: raise KeyboardInterrupt
    elif kbd_input in keys_raw: pass

    elif menu_state.wrtptr < ((app_state.columns + 2) * app_state.rows + 1):
        out = decode(kbd_input)
        p1 = menu_state.filewrite[:menu_state.wrtptr - menu_state.lenght]
        p2 = menu_state.filewrite[menu_state.wrtptr - menu_state.lenght:]
        menu_state.filewrite = f"{p1}{out}{p2}"
        menu_state.wrtptr += len(out)
        menu_state.auto_complete = False


 