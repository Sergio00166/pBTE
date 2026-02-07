# Code by Sergio00166

from data import ascii_map,ascii_replaced
from os import get_terminal_size
from wcwidth import wcwidth
from sys import stdout

# ANSI control codes
movcr = "\r\033[%d;%dH"
movtl = movcr%(0,0)
clr   = "\033[2K"
scr   = "\r\x1b[?25h"
hcr   = "\r\x1b[?25l"

def print(text):
    stdout.write(text)
    stdout.flush()


def text_selection(state, all_file):
    start, end = state.select[0][0], state.select[1][0]
    delta = state.select[1][1] - state.select[0][1]

    if state.line < state.rows + state.banoff: end += delta
    start, out = max(0, start - delta), []

    p0, p1, p2 = all_file[:start], all_file[start:end], all_file[end:]
    ctrl_len = len(f"{state.black}*{state.reset}")

    for x in p1:
        ctrl_len = str_len(x.replace(state.black, "").replace(state.reset, ""))
        x = rscp(x, [state.black, state.reset, state.slc])

        if x.endswith(f"{state.black}>{state.reset}"):
            x = f"{x[:-ctrl_len]}{state.reset}>{state.black}"

        elif x.startswith(f"{state.black}<{state.reset}"):
            x = f"{x[:-ctrl_len]}{state.reset}<{state.black}"

        out.append(f"{state.black}{x}{state.reset}")
    return p0 + out + p2


def str_len(self, tabsize=8):
    result, col, lenght = [], 0, 0

    for char in self:
        if char == "\t":
            space_count = tabsize - (col % tabsize)
            result.append(" " * space_count)
            lenght += space_count
            col += space_count
        else:
            result.append(char)
            char_width = wcwidth(char)
            lenght += char_width
    return lenght


def get_size():
    size = get_terminal_size()
    return size[1] - 2, size[0] - 2


def fixlenline(text, cursor, oldptr):
    lenght = len(text)
    if max(oldptr, cursor) > lenght: return lenght
    elif oldptr > cursor:            return oldptr
    else:                            return cursor


def sscp(arg,color):
    global ascii_map
    b, r = color; ext = []

    for x in arg:
        if ord(x) in ascii_map:
            ext.append(f"{b}{ascii_map[ord(x)]}{r}")

        elif str_len(x)>0: ext.append(x)
        else: ext.append(f"{b}�{r}")

    return "".join(ext)


def rscp(arg,color):
    global ascii_replaced

    if len(color) == 3:
        b, r, c = color
        b1 = r + b
        r1 = r + c
    else:
        b, r = color
        b1, r1 = b, r

    for x in ascii_replaced:
        arg = arg.replace(f"{b}{x}{r}", f"{r1}{x}{b1}")
    return arg

 