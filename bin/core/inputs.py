# Code by Sergio00166

from text_op import del_sel, select_add_start_str
from functions import calc_displacement
from re import split as resplit
from data import ascii_no_lfcr
from os import sep, read
from data import keys_raw


if sep == chr(92):  # Windows
    from msvcrt import getch as gch, kbhit
    from ctypes import windll

    kbdenc = f"cp{windll.kernel32.GetConsoleCP()}"

    def tty_read_stdin():
        out = [gch()]
        while kbhit(): out.append(gch())
        return b''.join(out)


else:  # Linux or POSIX
    from termios import TCSADRAIN, tcsetattr, tcgetattr
    from select import select as slsl
    from sys import stdin
    from tty import setraw
    from sys import stdin

    fd = stdin.fileno()
    old_settings = tcgetattr(fd)
    kbdenc = stdin.encoding

    def tty_read_stdin():
        old = (fd, TCSADRAIN, old_settings)
        setraw(fd, when=TCSADRAIN)

        out, rlist = [], True
        while rlist:
            out.append(read(fd, 4))
            rlist = slsl([fd], [], [], 0)[0]

        tcsetattr(*old)
        return b''.join(out)


# Avoid merging two control keys as an
# single one, keeps the rest unchanged
input_buffer = b""
def getch():
    global input_buffer

    if input_buffer:
        data = input_buffer
        input_buffer = b""
    else:
        data = tty_read_stdin()

    for k in keys_raw:
        if data.startswith(k):
            seq_len = len(k)
            input_buffer = data[seq_len:]
            return data[:seq_len]
    return data


def decode(key):
    out = key.decode(kbdenc)
    for x in ascii_no_lfcr:
        if chr(x) in out: return ""
    return out


def handle_text_input(state, key):
    out = decode(key)

    if state.select_mode and state.select:
        del_sel(state, True)
        state.cursor = 0

    pos = state.line + state.offset - state.banoff
    text = state.arr[pos]
    before_cursor = text[:state.cursor]
    after_cursor  = text[state.cursor:]

    out = out.replace("\t", state.indent)
    out_lines = resplit(r"[\n\r]", out)

    if not (state.select_mode and state.select) and len(out_lines) > 1:
        state.arr[pos] = before_cursor + out_lines[0]
    else:
        state.arr[pos] = before_cursor + out_lines[0] + after_cursor

    if len(out_lines) > 1:
        state.cursor = len(out_lines[-1])

        if not (state.select_mode and state.select):
            out_lines[-1] += after_cursor

        state.arr[pos + 1:pos + 1] = out_lines[1:]
        calc_displacement(state, out_lines, 1)
    else:
        state.cursor += len(out_lines[0])

    state.status_st = False
    state.select_mode = False
    state.select = []


 