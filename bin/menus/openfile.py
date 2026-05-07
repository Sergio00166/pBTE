# Code by Sergio00166

from functions import read_UTF8
from types import SimpleNamespace
from inputs import decode, getch
from data import keys, keys_raw
from upd_scr import menu_updsrc
from time import sleep as delay
from scr_utils import get_size
from threading import Thread
from os.path import dirname
from os import getcwd, sep
from glob import glob


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
            menu_state.openfile,
            menu_state.opentxt,
            menu_state.wrtptr,
            menu_state.lenght
        )
        menu_updsrc(app_state, mode)
        if sep != chr(92): setraw(fd, when=TCSADRAIN)


def exit(menu_state):
    global fd, old_settings



def open_file(app_state):
    global fd, old_settings, thr

    menu_state = SimpleNamespace(
        openfile = dirname(app_state.filename),
        opentxt = " Open: ",
        auto_complete = False,
        lenght = 0,
        wrtptr = 0,
        cmp_counter = 0,
        run = False,
        kill = False
    )
    if not menu_state.openfile.endswith("/"):
        menu_state.openfile += "/"

    menu_state.lenght = len(menu_state.opentxt) + 1
    menu_state.wrtptr = menu_state.lenght + len(menu_state.openfile)

    thr = Thread(target=updscr_thr, args=(app_state, menu_state))
    thr.daemon = True; thr.start()

    while True:
        if len(menu_state.openfile) < menu_state.wrtptr - menu_state.lenght:
            menu_state.wrtptr = len(menu_state.openfile) + menu_state.lenght
        try:
            menu_state.openfile = menu_state.openfile.replace(chr(92), "/")
            if sep != chr(92):
                old = (fd, TCSADRAIN, old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)

            mode = (
                menu_state.openfile,
                menu_state.opentxt,
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
    app_state.filename.removeprefix("//")


def menu_actions(app_state, menu_state, kbd_input):

    if menu_state.auto_complete and kbd_input == keys["return"]:
        menu_state.wrtptr = len(menu_state.openfile + menu_state.opentxt) + 2
        menu_state.auto_complete = False

    elif kbd_input == keys["arr_left"]:
        if not menu_state.wrtptr == menu_state.lenght:
            menu_state.wrtptr -= 1

    elif kbd_input == keys["arr_right"]:
        total = len(menu_state.openfile) + menu_state.lenght
        if not menu_state.wrtptr > total: menu_state.wrtptr += 1

    elif kbd_input in keys["start"]:
        menu_state.wrtptr = menu_state.lenght

    elif kbd_input in keys["end"]:
        menu_state.wrtptr = len(menu_state.openfile) + menu_state.lenght

    elif kbd_input == keys["tab"]:
        if (len(menu_state.openfile) == 0 or
           (sep == chr(92) and not ":/" in menu_state.openfile)
        ): return
        
        if not menu_state.auto_complete:
            menu_state.content = glob(menu_state.openfile + "*", recursive=False)

        if len(menu_state.content) > 0: menu_state.auto_complete = True

        if menu_state.cmp_counter >= len(menu_state.content):
            menu_state.cmp_counter = 0

        if menu_state.auto_complete:
            menu_state.openfile = menu_state.content[menu_state.cmp_counter]
            menu_state.cmp_counter += 1


    elif kbd_input == keys["ctrl+o"]:
        menu_state.openfile = glob(menu_state.openfile, recursive=False)[0]
        read_UTF8(app_state, menu_state.openfile)
        app_state.cursor, app_state.offset = 0,0
        app_state.oldptr, app_state.line   = 0,1
        app_state.status_st = False
        app_state.select = []
        raise KeyboardInterrupt


    elif kbd_input == keys["ctrl+n"]:
        app_state.cursor, app_state.oldptr = 0,0
        app_state.offset, app_state.line   = 0,1
        app_state.arr, app_state.select, app_state.status_st = [""], [], False
        app_state.filename = getcwd() + "/NewFile"
        raise KeyboardInterrupt


    elif kbd_input == keys["backspace"]:
        if not menu_state.wrtptr == menu_state.lenght:

            if menu_state.auto_complete:
                menu_state.openfile = menu_state.openfile.split("/")[:-1]
                menu_state.openfile = "/".join(menu_state.openfile) + "/"
                menu_state.wrtptr -= len(menu_state.openfile[-1]) - 1
                menu_state.auto_complete = False
            else:
                p1 = list(menu_state.openfile)
                p1.pop(menu_state.wrtptr - menu_state.lenght - 1)
                menu_state.openfile = "".join(p1)
                menu_state.wrtptr -= 1


    elif kbd_input == keys["delete"]:
        if menu_state.auto_complete:
            menu_state.openfile = menu_state.openfile.split("/")[:-1]
            menu_state.openfile = "/".join(menu_state.openfile) + "/"
            menu_state.wrtptr -= len(menu_state.openfile[-1]) - 1
            menu_state.auto_complete = False
        else:
            idx = menu_state.wrtptr - menu_state.lenght
            if idx >= len(menu_state.openfile): return   
            p1 = list(menu_state.openfile)
            p1.pop(idx) # Remove last char
            menu_state.openfile = "".join(p1)


    elif kbd_input == keys["ctrl+c"]: raise KeyboardInterrupt
    elif kbd_input in keys_raw: pass

    elif menu_state.wrtptr < ((app_state.columns + 2) * app_state.rows + 1):
        out = decode(kbd_input)
        p1 = menu_state.openfile[:menu_state.wrtptr - menu_state.lenght]
        p2 = menu_state.openfile[menu_state.wrtptr - menu_state.lenght:]
        menu_state.openfile = f"{p1}{out}{p2}"
        menu_state.wrtptr += len(out)
        menu_state.auto_complete = False


 