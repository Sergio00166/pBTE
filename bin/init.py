# Code by Sergio00166

VERSION = "v0.8.2.1"

if not __name__ == "__main__":
    from os import getcwd, sep, environ
    from sys import argv, path

    root = path[0] + sep + "bin" + sep
    path.append(root + "core")
    path.append(root + "menus")

    from os.path import abspath, isdir, join
    from types import SimpleNamespace
    from data import keys, keys_raw
    from functions import read_UTF8
    from keys_func import keys_func
    from time import sleep as delay
    from scr_utils import get_size
    from upd_scr import update_scr
    from threading import Thread
    from inputs import getch
    from glob import glob
    

    rows, columns = get_size()

    if sep != chr(92):  # If OS is LINUX
        from termios import TCSADRAIN, tcsetattr, tcgetattr
        from sys import stdin
        from tty import setraw

        fd = stdin.fileno()
        old_settings = tcgetattr(fd)

    app_state = SimpleNamespace(
        black = "\x1b[106m\x1b[30m",
        bnc = "\x1b[42m\x1b[30m",
        slc = "\x1b[103m\x1b[30m",
        reset = "\x1b[0m",
        banner = ["pBTE", VERSION],
        filename = join(getcwd(), "NewFile"),
        arr = [""],
        codec = "UTF-8",
        lnsep = "\n",
        comment = ["#", ""],
        indent = "\t",
        cursor = 0,
        oldptr = 0,
        line = 1,
        offset = 0,
        banoff = 1,
        rows = rows,
        columns = columns,
        select = [],
        select_mode = False,
        copy_buffer = "",
        status = "",
        status_st = False,
    )

    if len(argv) > 1:
        files = [glob(x, recursive=False) for x in argv[1:]]
        files = [abspath(i) for x in files for i in x if not isdir(i)]
        files = [x.replace(sep, "/") for x in files]
        for _ in range(len(files)):
            try:
                read_UTF8(app_state, files[0])
                files = files[1:]
                break
            except: pass
    else: files = []

    # Change TTY buffer
    print("\x1b[?1049h", end="")


 