# Code by Sergio00166

VERSION = "v0.8.0.2"

if not __name__ == "__main__":
    from os import getcwd, sep, environ
    from sys import argv, path

    # Add all file structure to import path
    root = path[0] + sep + "bin" + sep
    path.append(sep.join([path[0], "bin", "lib.zip"]))
    path.append(root + "core")
    path.append(root + "menus")

    from colorama import init, Fore, Back, Style, deinit
    from os.path import abspath, isdir, join
    from types import SimpleNamespace
    from functions import read_UTF8
    from keys_func import keys_func
    from time import sleep as delay
    from scr_utils import get_size
    from upd_scr import update_scr
    from threading import Thread
    from inputs import getch
    from glob import glob
    from data import keys

    if not sep == chr(92):  # If OS is LINUX
        # Get default values for TTY
        from termios import TCSADRAIN, tcsetattr, tcgetattr
        from sys import stdin
        from tty import setraw

        fd = stdin.fileno()
        old_settings = tcgetattr(fd)

    init(autoreset=False, convert=True)
    rows, columns = get_size()

    # --- Application state ---
    app_state = SimpleNamespace(
        # Colors
        black = Back.LIGHTCYAN_EX + Fore.BLACK,
        bnc = Back.GREEN + Fore.BLACK,
        slc = Back.LIGHTYELLOW_EX + Fore.BLACK,
        reset = Style.RESET_ALL,
        # Info
        banner = ["pBTE", VERSION],
        # File
        filename = join(getcwd(), "NewFile"),
        arr = [""],
        codec = "UTF-8",
        lnsep = "\n",
        # Editor
        comment = ["#", ""],
        indent = "\t",
        # Cursor
        cursor=0,
        oldptr=0,
        line=1,
        offset=0,
        banoff=1,
        # Display
        rows=rows,
        columns=columns,
        # Selection
        select=[],
        select_mode=False,
        copy_buffer="",
        # Status
        status="",
        status_st=False,
        # Keys
        keys=keys
    )
    deinit()

    # --- Load file if passed as argument ---
    if len(argv) > 1:
        files = [glob(x, recursive=False) for x in argv[1:]]
        files = [abspath(i) for x in files for i in x if not isdir(i)]
        files = [x.replace(sep, "/") for x in files]
        for _ in range(len(files)):
            try:
                read_UTF8(state, files[0])
                filename = files[0]
                files = files[1:]
                break
            except: pass
    else: files = []

    # --- Switch to alternate screen buffer ---
    print("\x1b[?1049h", end="")
    

