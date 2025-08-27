# Code by Sergio00166

from scr_funcs import *
from sys import stdout
from os import sep

# ANSI control codes
movcr = "\r\033[%d;%dH"
cls   = "\033[2K"
scr   = "\r\x1b[?25h"
hcr   = "\r\x1b[?25l"

def print(text):
    stdout.write(text)
    stdout.flush()


def text_selection(buffer, select, rows, banoff, line, color, sel_color, reset, columns):
    (start_line, _), (end_line, _) = select
    span = end_line - _

    head = max(start_line - span, 0)
    tail = end_line + (span if line < rows + banoff else 0)

    highlight, star_len = [], len(color + "*" + reset)
    for raw in buffer[head:tail]:
        # Strip and re-apply selection markers
        clean = rscp(raw, [color, reset, sel_color])
        if clean.endswith(color + ">" + reset):
            clean = clean[:-star_len] + reset + ">" + color
        elif clean.startswith(color + "<" + reset):
            clean = clean[:-star_len] + reset + "<" + color

        highlight.append(color + clean + reset)

    return buffer[:head] + highlight + buffer[tail:]


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
    menu_body = cls + bnc+header + " "*pad + filename + " " + reset
    menu_text = menu_body + "\n" + cls + ("\n" + cls).join(screen_lines)

    if rrw: return menu_text

    # Print and move cursor
    print(hcr + menu_text + scr + movcr%(line + banoff, cursor+1))
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

    # Try building raw menu for sizing
    try:
        raw_menu = update_scr(
            black, bnc, slc, reset, status,
            banoff, offset, line, 0, arr,
            banner, filename, rows, columns,
            status_st, rrw=True
        )
    except Exception: return rows, columns

    # Truncate to fit height
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

    print(
        hcr + menu + "\n"
        + bnc + content + scr
        + movcr % (rows + 2, wrtptr + 1)
    )
    return rows, columns


