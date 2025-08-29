# Code by Sergio00166

from scr_funcs import *
from sys import stdout
from os import sep

# ANSI control codes
movcr = "\r\033[%d;%dH"
movtl = movcr%(0,0)
clr   = "\033[2K"
scr   = "\r\x1b[?25h"
hcr   = "\r\x1b[?25l"

def print(text):
    stdout.write(text)
    stdout.flush()


def text_selection(all_file, select, rows, banoff, line, black, slc, reset, columns):
    start, end = select[0][0], select[1][0]
    delta = select[1][1] - select[0][1]

    if line < rows + banoff:
        end += delta
    start = max(0, start - delta)

    p0, p1, p2 = all_file[:start], all_file[start:end], all_file[end:]
    out, ctrl_len = [], len(black + "*" + reset)

    for x in p1:
        ctrl_len = str_len(x.replace(black, "").replace(reset, ""))
        x = rscp(x, [black, reset, slc])
        if x.endswith(black + ">" + reset):
            x = x[:-ctrl_len] + reset + ">" + black
        elif x.startswith(black + "<" + reset):
            x = x[:-ctrl_len] + reset + "<" + black
        out.append(black + x + reset)

    return p0 + out + p2


def update_scr(
    black, bnc, slc, reset, status,
    banoff, offset, line, cursor,
    lines, banner, filename, rows,
    columns, status_st, rrw=False,
    select=None, hlg_str=""
):
    # Header: position + banner text + status
    pos    = f" {line + offset - banoff}  "
    stat   = (" " + banner[1]) if not status_st else ("  " + status)
    header = pos + " " + banner[0] + stat + "    "

    avail = columns - len(header)
    if avail < 24:
        header = ""
        filename = fixfilename(filename, columns).replace(sep, "/")
        filename += " " * (columns - len(filename))
        pad = 1
    else:
        filename = fixfilename(filename, avail).replace(sep, "/")
        pad = columns - len(header) - len(filename) + 1

    # Convert array of lines and adjust cursor
    screen_lines, cursor = scr_arr2str(
        lines, line, offset, cursor,
        black, reset, columns, rows, banoff
    )
    # Highlight selection or string if requested
    if select:
        screen_lines = text_selection(
            screen_lines, select, rows, banoff,
            line, black, slc, reset, columns
        )
    elif hlg_str:
        screen_lines = [
            ln.replace(hlg_str, black + hlg_str + reset)
            for ln in screen_lines
        ]

    # Pad to full height
    screen_lines += [" "] * max(0, rows - len(screen_lines) + 1)

    # Assemble the full menu
    menu_body = clr + bnc+header + " "*pad + filename + " " + reset
    menu_text = menu_body + "\n" + clr + ("\n" + clr).join(screen_lines)

    if rrw: return menu_text

    # Print and move cursor
    print(
        hcr + movtl + menu_text + scr +
        movcr%(line + banoff, cursor+1)
    )
    if hlg_str: return cursor



def menu_updsrc(args, mode=None, redraw=False):
    (black, bnc, slc, reset, status,
     banoff, offset, line, cursor,
     arr, banner, filename,
     rows, columns, status_st) = args

    old_size = (rows, columns)
    rows, columns = get_size()

    # Screen too small?
    if rows < 4 or columns < 24:
        print("\r\033cTerminal too small")
        return rows, columns

    # No change in size and not forced redraw
    if old_size == (rows, columns) and not redraw:
        return rows, columns

    # Clear if first draw, otherwise bail if no mode
    if not redraw: print("\r\033[3J")
    elif not mode: return rows, columns

    filetext, opener, wrtptr, length = mode
    content = opener + filetext

    # Get raw screen string
    raw_menu = update_scr(
        black, bnc, slc, reset, status,
        banoff, offset, line, 0, arr,
        banner, filename, rows, columns,
        status_st, rrw=True
    )

    # Truncate to leave space for menu
    lines = raw_menu.split("\n")[: rows + banoff]
    menu = "\n".join(lines)

    # Reposition write pointer in content
    wrtptr, content = fix_cursor_pos(
        content, wrtptr - 1, columns, slc, reset + bnc
    )
    # Pad content line to full width
    curr_len = str_len(
        content.replace(slc, "")
        .replace(reset + bnc, "")
    )
    if curr_len != columns:
        content += " "*(columns - curr_len + 2)

    # Print and move cursor
    print(
        hcr + movtl +  menu + "\n"
        + bnc + content + scr
        + movcr % (rows + 2, wrtptr + 1)
    )
    return rows, columns


