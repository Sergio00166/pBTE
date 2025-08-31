# Code by Sergio00166

from functions import read_UTF8, write_UTF8
from types import SimpleNamespace
from inputs import decode, getch
from upd_scr import menu_updsrc
from time import sleep as delay
from scr_utils import get_size
from threading import Thread
from glob import glob
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
                menu_state.filewrite,
                menu_state.saveastxt,
                menu_state.wrtptr,
                menu_state.lenght
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


def save_as(app_state):
    global fd, thr, old_settings

    # Create menu state object
    menu_state = SimpleNamespace(
        saveastxt = " Save as: ",
        filewrite = app_state.filename,
        lenght = 0,
        wrtptr = 0,
        complete = False,
        cmp_counter = 0,
        run = False,
        kill = False
    )
    menu_state.lenght = len(menu_state.saveastxt) + 1
    menu_state.wrtptr = menu_state.lenght + len(menu_state.filewrite)

    thr = Thread(target=updscr_thr, args=(app_state, menu_state))
    menu_state.run, menu_state.kill = False, False
    thr.daemon = True
    thr.start()

    while True:
        # Fix when the cursor is out
        if len(menu_state.filewrite) < menu_state.wrtptr - menu_state.lenght:
            menu_state.wrtptr = len(menu_state.filewrite) + menu_state.lenght
        try:
            # Force use LINUX dir separator
            menu_state.filewrite = menu_state.filewrite.replace(chr(92), "/")
            # If OS is LINUX restore TTY to it default values
            if not sep == chr(92):
                old = (fd, TCSADRAIN, old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            mode = (
                menu_state.filewrite,
                menu_state.saveastxt,
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

            # Reset error message
            if app_state.status == "ERROR":
                app_state.status_st = False

            if key == app_state.keys["tab"]:
                if not (
                    len(menu_state.filewrite) == 0
                    or (sep == chr(92) and not ":/" in menu_state.filewrite)
                ):
                    if not menu_state.complete:
                        content = glob(menu_state.filewrite + "*", recursive=False)
                    if len(content) > 0:
                        menu_state.complete = True
                    if menu_state.cmp_counter >= len(content):
                        menu_state.cmp_counter = 0
                    if menu_state.complete:
                        menu_state.filewrite = content[menu_state.cmp_counter]
                        menu_state.cmp_counter += 1
                    else:
                        menu_state.filewrite = content[0]

            elif menu_state.complete and key == app_state.keys["return"]:
                menu_state.wrtptr = (
                    len(menu_state.filewrite) + len(menu_state.saveastxt) + 2
                )
                menu_state.complete = False

            # Ctrl + S (confirms) or Ctrl + B backup
            elif key in (
                app_state.keys["ctrl+s"], 
                app_state.keys["ctrl+b"]
            ):
                save_file = menu_state.filewrite +\
                    (".bak" if key == app_state.keys["ctrl+b"] else "")
                try:
                    write_UTF8(
                        save_file, 
                        app_state.codec,
                        app_state.lnsep,
                        app_state.arr
                    )
                    if key == app_state.keys["ctrl+b"]:
                        app_state.status = "BCKPd"
                    else:
                        app_state.status = "SAVED"
                        app_state.filename = menu_state.filewrite
                    app_state.status_st = True
                    break
                except:
                    app_state.status, app_state.status_st = "ERROR", True

            elif key in (
                app_state.keys["ctrl+p"],
                app_state.keys["ctrl+a"]
            ):
                tmp, codec, lnsep = read_UTF8(menu_state.filewrite)
        
                if key == app_state.keys["ctrl+a"]:
                    output = list(app_state.arr + tmp)
                elif key == app_state.keys["ctrl+p"]:
                    output = list(app_state.tmp + arr)

                write_UTF8(
                    menu_state.filewrite, 
                    codec, lnsep, output
                )
                app_state.status = app_state.bnc + "ADDED"
                app_state.status_st = True
                break

            elif key == app_state.keys["ctrl+c"]: break

            elif key == app_state.keys["delete"]:
                if not menu_state.wrtptr == menu_state.lenght:
                    if menu_state.complete:
                        menu_state.filewrite = menu_state.filewrite.split("/")[:-1]
                        menu_state.filewrite = "/".join(menu_state.filewrite) + "/"
                        menu_state.wrtptr -= len(menu_state.filewrite[-1]) - 1
                        menu_state.complete = False
                    else:
                        p1 = list(menu_state.filewrite)
                        p1.pop(menu_state.wrtptr - menu_state.lenght - 1)
                        menu_state.filewrite = "".join(p1)
                        menu_state.wrtptr -= 1

            elif key == app_state.keys["arr_left"]:
                if not menu_state.wrtptr == menu_state.lenght:
                    menu_state.wrtptr -= 1

            elif key == app_state.keys["arr_right"]:
                if (
                    not menu_state.wrtptr
                    > len(menu_state.filewrite) + menu_state.lenght
                ):
                    menu_state.wrtptr += 1

            elif key == app_state.keys["supr"]:
                if menu_state.complete:
                    menu_state.filewrite = menu_state.filewrite.split("/")[:-1]
                    menu_state.filewrite = "/".join(menu_state.filewrite) + "/"
                    menu_state.wrtptr -= len(menu_state.filewrite[-1]) - 1
                    menu_state.complete = False
                else:
                    p1 = list(menu_state.filewrite)
                    p1.pop(menu_state.wrtptr - menu_state.lenght)
                    menu_state.filewrite = "".join(p1)

            elif key in app_state.keys["start"]:
                menu_state.wrtptr = menu_state.lenght

            elif key in app_state.keys["end"]:
                menu_state.wrtptr = len(menu_state.filewrite) + menu_state.lenght

            else:  # Rest of keys
                if menu_state.wrtptr < ((app_state.columns + 2) * app_state.rows + 1):
                    out = decode(key)
                    p1 = menu_state.filewrite[: menu_state.wrtptr - menu_state.lenght]
                    p2 = menu_state.filewrite[menu_state.wrtptr - menu_state.lenght :]
                    menu_state.filewrite = p1 + out + p2
                    menu_state.wrtptr += len(out)
                    menu_state.complete = False

        except OSError:
            app_state.status, app_state.status_st = "ERROR", True
        except: pass

    exit(menu_state)  # Reset

