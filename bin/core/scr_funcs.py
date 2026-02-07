# Code by Sergio00166

from os.path import split as psplit
from wcwidth import wcwidth
from os import sep
from scr_utils import *


# Expands tabulators and splits the text in parts
def wrap(text, columns, tabsize=8, cursor=None):
    buffer,counter,col = "", -1, 0
    result,pos,ptr = [], 0, 0
    extra = cursor != None

    def handle_char(char, char_width):
        nonlocal buffer, counter, col, result, ptr, pos

        if counter + char_width > columns:
            result.append(buffer)
            if ptr - counter > 0:
                ptr -= counter
                pos += 1

            buffer, counter = char, char_width
        else:
            buffer += char
            counter += char_width

        col += char_width

    for p, char in enumerate(text):
        if char == "\t":
            space_count = tabsize - (col % tabsize)
            expanded = " " * space_count
            if extra and cursor > p: ptr += space_count
            for x in expanded: handle_char(x, 1)
        else:
            char_width = wcwidth(char)
            if char_width < 1: char_width = 1
            if extra and cursor > p: ptr += char_width
            handle_char(char, char_width)

    if buffer: result.append(buffer)
    return (result, ptr, pos) if extra else (result)


def fix_arr_line_len(state, sub_arr):
    fix, out = 0 // (state.columns + 2), []

    for text in sub_arr:
        text = text[:state.columns + 2]
        wrapped_text = wrap(text, state.columns)

        if len(wrapped_text) == 0:
            text = ""
        elif fix == len(wrapped_text):
            text = wrapped_text[fix - 1]
        else:
            text = wrapped_text[fix]

        text = sscp(text, [state.black, state.reset])
        if (len(wrapped_text) - fix) > 1:
            text += f"{state.black}>{state.reset}"

        out.append(text)
    return out


def fix_cursor_pos(text,cursor,columns,black,reset):
    text = text[: cursor + columns + 2]
    wrapped_text, cursor, pos = wrap(text, columns, cursor=cursor)

    if not len(wrapped_text) == 0:
        if pos > len(wrapped_text) - 1: pos =- 1
        text = wrapped_text[pos]
        text = sscp(text, (black, reset))

        if pos > 0:
            text = f"{black}<{reset}{text}"
            if not pos == len(wrapped_text) - 1:
                text += f"{black}>{reset}"

        elif len(wrapped_text) > 1:
            text += f"{black}>{reset}"

    else: text = ""
    return cursor, text


def scr_arr2str(state):
    text = state.arr[state.line + state.offset - state.banoff]
    cursor, text = fix_cursor_pos(
        text, state.cursor, state.columns, state.black, state.reset
    )
    sub_arr = state.arr[state.offset : state.offset + state.rows + state.banoff]
    sub_arr = fix_arr_line_len(state, sub_arr)
    sub_arr[state.line - state.banoff] = text
    return sub_arr, cursor


def fixfilename(path, lenght):
    if len(path) <= lenght: return path
    dirname, basename = psplit(path)

    if len(path) <= lenght: return path
    available_lenght = lenght - len(basename) - 1

    if available_lenght <= 0: return basename[:lenght - 1] + "*"
    parts = dirname.split(sep)

    while len(parts) > 0 and len(sep.join(parts)) > available_lenght: parts.pop(0)
    if len(parts) == 0: compacted_path = basename
    else: compacted_path = f"{sep.join(parts)}{sep}{basename}"
    return compacted_path

 