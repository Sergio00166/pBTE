# Code by Sergio00166

from functions import calc_displacement
from actions import up,down
from text_op import *


def paste(state):
    if not len(state.copy_buffer) == 0:
        if not state.select_mode or len(state.select) == 0:
            pos = state.line + state.offset - state.banoff
            text = state.arr[pos]
            p1, p2 = text[:state.cursor], text[state.cursor:]

            if isinstance(state.copy_buffer, list):
                state.arr[pos] = p1 + state.copy_buffer[0]

                for i, new_line in enumerate(state.copy_buffer[1:], start=1):
                    state.arr.insert(pos + i, new_line)

                state.arr[pos + len(state.copy_buffer) - 1] += p2
                calc_displacement(state, state.copy_buffer[1:])
                state.cursor = len(state.copy_buffer[-1])
            else:
                state.arr[pos] = p1 + state.copy_buffer + p2
                state.cursor += len(state.copy_buffer)
        else:
            start = sum(state.select[0])
            del_sel(state)

            if isinstance(state.copy_buffer, list):
                for i, new_line in enumerate(state.copy_buffer):
                    state.arr.insert(start + i, new_line)

                calc_displacement(state, state.copy_buffer, 1)
                state.cursor = len(state.copy_buffer[-1])
            else:
                state.arr.insert(start, state.copy_buffer)
                state.cursor = len(state.copy_buffer)
        state.status_st = False


def cut(state):
    pos = state.line + state.offset - state.banoff
    text = state.arr[pos]

    if state.select_mode and state.select:
        start = max(sum(state.select[0]) - 1, 0)
        state.copy_buffer = state.arr[start:sum(state.select[1])]
        if start > 0: state.copy_buffer = state.copy_buffer[1:]

        del_sel(state)
        state.select = []
        state.select_mode = False
    else:
        if state.cursor == 0:
            if pos == len(state.arr) - 1:
                if text != "":
                    state.copy_buffer = text
                    state.arr[pos] = ""
            else:
                state.copy_buffer = text
                state.arr.pop(pos)

        elif state.cursor == len(text):
            if pos < len(state.arr) - 1:
                state.copy_buffer = state.arr.pop(pos + 1)
        else:
            state.arr[pos] = text[:state.cursor]
            state.copy_buffer = text[state.cursor:]

    if isinstance(state.copy_buffer, list) and len(state.copy_buffer) == 1:
        state.copy_buffer = state.copy_buffer[0]


def copy(state):
    if state.select_mode and state.select:
        start = max(sum(state.select[0]) - 1, 0)
        state.copy_buffer = state.arr[start:sum(state.select[1])]

        if start > 0:
            state.copy_buffer = state.copy_buffer[1:]

        state.select = []
        state.select_mode = False
    else:
        pos = state.line + state.offset - state.banoff
        text = state.arr[pos]

        if state.cursor == len(text):
            if pos < len(state.arr) - 1:
                state.copy_buffer = state.arr[pos + 1]
        else:   state.copy_buffer = text[state.cursor:]

    if isinstance(state.copy_buffer, list) and len(state.copy_buffer) == 1:
        state.copy_buffer = state.copy_buffer[0]


def indent(state):
    pos = state.line + state.offset - state.banoff
    text = state.arr[pos]

    if state.select_mode and state.select:  
        select_add_start_str(state, state.indent)

        if state.arr[pos] != text:
            state.cursor += len(state.indent)
    else:
        p1 = text[:state.cursor] 
        p2 = text[state.cursor:]

        state.arr[pos] = p1 + state.indent + p2
        state.cursor += len(state.indent)


def dedent(state):
    pos = state.line + state.offset - state.banoff
    orig = state.arr[pos]

    if not state.select_mode or len(state.select) == 0:
        text = state.arr[pos]
        start = text[:state.cursor]

        if start.endswith(state.indent):
            start = start[:-len(state.indent)]
            state.arr[pos] = start + text[state.cursor:]
    else:
        select_add_start_str(state, state.indent, True)

    if state.arr[pos] != orig:
        state.cursor -= len(state.indent)


def comment_func(state):
    pos = state.line + state.offset - state.banoff
    orig = state.arr[pos]

    if not state.select_mode or len(state.select) == 0:
        indent_part, content_part = cmt_w_ind(state.arr[pos], state.indent)
        state.arr[pos] = indent_part + state.comment[0] + content_part + state.comment[1]
    else:
        select_add_start_str(state, state.comment)

    if state.arr[pos] != orig:
        state.cursor += len(state.comment[0])


def uncomment_func(state):
    pos = state.line + state.offset - state.banoff
    orig = state.arr[pos]

    if not state.select_mode or len(state.select) == 0:
        indent_part, content_part = cmt_w_ind(orig, state.indent)
 
        if content_part.startswith(state.comment[0]):
            content_part = content_part[len(state.comment[0]):]

        if content_part.endswith(state.comment[1]):
            lencmt = len(state.comment[1])
            if lencmt: content_part = content_part[:-lencmt]

        state.arr[pos] = indent_part + content_part
    else:
        select_add_start_str(state, state.comment, True)

    if state.arr[pos] != orig:
        state.cursor -= len(state.comment[0])


 