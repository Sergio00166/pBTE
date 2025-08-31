# Code by Sergio00166

from text_op import del_sel, select_add_start_str
from functions import calc_displacement
from re import split as resplit
from data import ascii_no_lfcr
from os import sep, read


# Platform-specific imports and setup
if sep == chr(92):  # Windows
    from ctypes import windll
    kbdenc = "cp" + str(windll.kernel32.GetConsoleCP())
else:  # Linux or POSIX
    from sys import stdin
    kbdenc = stdin.encoding


# Platform-specific key input handling
if sep == chr(92):  # Windows
    from msvcrt import getch as gch, kbhit

    def getch():
        """Get character input on Windows"""
        out = gch()
        while kbhit():
            out += gch()
        return out
else:  # Linux or POSIX
    from termios import TCSADRAIN, tcsetattr, tcgetattr
    from sys import stdin
    from tty import setraw
    from select import select as slsl

    fd = stdin.fileno()
    old_settings = tcgetattr(fd)

    def getch():
        """Get character input on Linux/POSIX"""
        old = (fd, TCSADRAIN, old_settings)
        setraw(fd, when=TCSADRAIN)
        out, rlist = b"", True
        
        while rlist:
            out += read(fd, 8)
            rlist = slsl([fd], [], [], 0)[0]
        
        tcsetattr(*old)
        return out


def decode(key):
    """Decode key input and filter out control characters"""
    out = key.decode(kbdenc)
    for x in ascii_no_lfcr:
        if chr(x) in out:
            return ""
    return out


def handle_text_input(state, key):
    """Handle text input and character insertion"""
    out = decode(key)
    
    if state.select_mode and state.select:
        if out == "\t":
            # Handle tab indentation for selection
            select_add_start_str(state, state.indent)
            return
        else:
            # Delete selection and insert character
            args = (state.select, state.arr, state.banoff, True)
            del_sel(state)
            state.cursor = 0  # Reset cursor value
    
    pos = state.line + state.offset - state.banoff
    text = state.arr[pos]  # Get current line
    before_cursor, after_cursor = text[:state.cursor], text[state.cursor:]
    
    # Replace tabs with spaces if needed
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
        
        # Calculate new position after insertion
        calc_displacement(state, out_lines, 1)
    else:
        state.cursor += len(out_lines[0])

    state.status_st = False
    state.select_mode = False
    state.select = []

