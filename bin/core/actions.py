# Code by Sergio00166

from text_op import *
from scr_utils import fixlenline


def down(state):
    if state.select_mode:
        selection_start = [state.line - state.banoff, state.offset]
        original_position = state.line + state.offset

    if state.line + state.offset != len(state.arr) + state.banoff - 1:
        if state.line != state.rows + state.banoff:
            state.line += 1
        elif state.line + state.offset != len(state.arr) + 1:
            state.offset += 1

        current_text = state.arr[state.line + state.offset - state.banoff]
        state.cursor = fixlenline(current_text, state.cursor, state.oldptr)

    if state.select_mode:
        selection_end = [state.line - state.banoff, state.offset]
        if sum(selection_end) < original_position:
            selection_end[0] += 1

        if len(state.select) == 0:
            state.select = [selection_start, selection_end]
        else:
            state.select[1] = selection_end
    else:   state.select = []


def up(state):
    if state.select_mode:
        selection_end = [state.line - state.banoff, state.offset]

    if state.line != state.banoff: state.line -= 1
    elif state.offset > 0: state.offset -= 1

    current_text = state.arr[state.line + state.offset - state.banoff]
    state.cursor = fixlenline(current_text, state.cursor, state.oldptr)

    if state.select_mode:
        selection_start = [state.line - state.banoff, state.offset]
        if len(state.select) == 0:
            state.select = [selection_start, selection_end]
        else:
            state.select[0] = selection_start
    else:   state.select = []


def left(state):
    if state.cursor != 0:
        state.cursor -= 1
        state.oldptr = state.cursor

    elif state.line + state.offset > state.banoff:
        if state.line > 1:     state.line   -= 1
        elif state.offset > 0: state.offset -= 1

        current_text = state.arr[state.line + state.offset - state.banoff]
        state.cursor = len(current_text)


def right(state):
    current_text = state.arr[state.line + state.offset - state.banoff]

    if state.cursor < len(current_text):
        state.cursor += 1
        state.oldptr = state.cursor
    elif state.offset + state.line <= len(state.arr) - 1:
        if state.line > state.rows: state.offset += 1
        else:                       state.line   += 1
        state.cursor = 0


def backspace(state):
    pos = state.line + state.offset - state.banoff
    current_text = state.arr[pos]

    if not state.select_mode or len(state.select) == 0:
        if state.cursor != 0:
            text_chars = list(current_text) + [""]
            try:    text_chars.pop(state.cursor - 1)
            except: text_chars.pop(state.cursor)
            current_text = "".join(text_chars)
            state.cursor -= 1

        elif state.offset + state.line != 1:
            previous_text = state.arr[pos - 1]
            state.arr[pos - 1] = previous_text + current_text

            state.arr.pop(pos)
            state.cursor = len(previous_text)
            current_text = previous_text + current_text

            if state.offset == 0: state.line -= 1
            else: state.offset -= 1

        state.arr[state.line + state.offset - state.banoff] = current_text
    else:
        del_sel(state)
        state.cursor = 0
        state.select_mode = False
        state.select = []
    state.status_st = False


def supr(state):
    idx = state.line + state.offset - state.banoff
    current_text = state.arr[idx]

    if not state.select_mode or len(state.select) == 0:
        text_chars = list(current_text)

        if state.cursor < len(text_chars) and len(text_chars) > 0:
            text_chars.pop(state.cursor)
            current_text = "".join(text_chars)
            state.arr[idx] = current_text

        elif state.cursor >= len(text_chars) and idx + 1 < len(state.arr):
            next_line = state.arr[idx + 1]
            merged_line = current_text + next_line
            state.arr[idx] = merged_line
            state.arr.pop(idx + 1)
    else:
        del_sel(state)
        state.cursor = 0


def newline(state):
    pos = state.line + state.offset - state.banoff
    current_text = state.arr[pos]

    if not state.select_mode or len(state.select) == 0:
        before_cursor = current_text[:state.cursor]
        after_cursor = current_text[state.cursor:]

        state.arr[pos] = before_cursor
        state.arr.insert(pos + 1, after_cursor)

        if state.line < state.rows: state.line   += 1
        else:                       state.offset += 1
        state.cursor = 0
    else:
        del_sel(state, True)
        state.cursor = 0
        state.select_mode = False
        state.select = []


def newline(state):
    if state.select_mode and len(state.select) > 0:
        del_sel(state)
        if len(state.arr) == 0: return

    pos = state.line + state.offset - state.banoff
    text = state.arr[state.line+state.offset-state.banoff]
 
    if not len(text) == 0:
        state.arr.insert(pos, text[:state.cursor])
        text = text[state.cursor:]; state.cursor = 0
    else:
        state.arr.insert(pos, "")

    if state.line > state.rows: state.offset += 1
    else:                       state.line   += 1

    state.arr[state.line + state.offset - state.banoff] = text
    state.status_st = False

 