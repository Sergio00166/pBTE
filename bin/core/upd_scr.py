# Code by Sergio00166

from scr_funcs import *
from os import sep


def update_scr(state, rrw=False, hlg_str=""):
    pos    = f" {state.line + state.offset - state.banoff}  "
    stat   = (" " + state.banner[1]) if not state.status_st else ("  " + state.status)
    header = pos + " " + state.banner[0] + stat + "    "

    avail = state.columns - len(header)
    if avail < 24:
        header,pad = "",1
        filename = fixfilename(state.filename, state.columns).replace(sep, "/")
        filename += " " * (state.columns - len(filename))
    else:
        filename = fixfilename(state.filename, avail).replace(sep, "/")
        pad = state.columns - len(header) - len(filename) + 1

    screen_lines, cursor = scr_arr2str(state)
    if state.select_mode and state.select:
        screen_lines = text_selection(state, screen_lines)
    elif hlg_str:
        screen_lines = [
            ln.replace(hlg_str, state.black + hlg_str + state.reset)
            for ln in screen_lines
        ]

    screen_lines += [" "] * max(0, state.rows - len(screen_lines) + 1)
    menu_body = clr + state.bnc+header + " "*pad + filename + " " + state.reset
    menu_text = menu_body + "\n" + clr + ("\n" + clr).join(screen_lines)

    if rrw: return menu_text
    print(
        hcr + movtl + menu_text + scr +
        movcr%(state.line + state.banoff, cursor+1)
    )
    if hlg_str: return cursor



def menu_updsrc(app_state, mode=None, redraw=False):
    old_size = (app_state.rows, app_state.columns)
    app_state.rows, app_state.columns = get_size()

    if app_state.rows<4 or app_state.columns<24:
        print("\r\033cTerminal too small"); return

    if old_size==(app_state.rows, app_state.columns) and not redraw: return

    if not redraw: print("\r\033[3J")
    elif not mode: return

    filetext, opener, wrtptr, length = mode
    content = opener + filetext

    raw_menu = update_scr(app_state, rrw=True)

    lines = raw_menu.split("\n")[:app_state.rows + app_state.banoff]
    menu = "\n".join(lines)

    wrtptr, content = fix_cursor_pos(
        content, wrtptr-1, app_state.columns, app_state.slc, app_state.reset + app_state.bnc
    )
    curr_len = str_len(
        content.replace(app_state.slc, "")
        .replace(app_state.reset + app_state.bnc, "")
    )
    if not curr_len==app_state.columns: 
        content += " "*(app_state.columns - curr_len + 2)

    print(
        hcr + movtl + menu + "\n" +
        app_state.bnc + content + scr +
        movcr % (app_state.rows + 2, wrtptr + 1)
    )

 