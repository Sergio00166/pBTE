# Code by Sergio00166

from text_op import *
from scr_utils import fixlenline


def down(state):
    """Move cursor down one line"""
    if state.select_mode:
        selection_start = [state.line - state.banoff, state.offset]
        original_position = state.line + state.offset
    
    # Move down if not at the end
    if state.line + state.offset != len(state.arr) + state.banoff - 1:
        if state.line != state.rows + state.banoff:
            state.line += 1
        elif state.line + state.offset != len(state.arr) + 1:
            state.offset += 1
        
        # Update cursor position for current line
        current_text = state.arr[state.line + state.offset - state.banoff]
        state.cursor = fixlenline(current_text, state.cursor, state.oldptr)
    
    # Handle selection mode
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
    """Move cursor up one line"""
    if state.select_mode:
        selection_end = [state.line - state.banoff, state.offset]
    
    # Move up if possible
    if state.line != state.banoff: state.line -= 1
    elif state.offset > 0: state.offset -= 1
    
    # Update cursor position for current line
    current_text = state.arr[state.line + state.offset - state.banoff]
    state.cursor = fixlenline(current_text, state.cursor, state.oldptr)
    
    # Handle selection mode
    if state.select_mode:
        selection_start = [state.line - state.banoff, state.offset]
        if len(state.select) == 0:
            state.select = [selection_start, selection_end]
        else:
            state.select[0] = selection_start
    else:   state.select = []


def left(state):
    """Move cursor left one character"""
    if state.cursor != 0:
        state.cursor -= 1
        state.oldptr = state.cursor

    elif state.line + state.offset > state.banoff:
        # Move to end of previous line
        if state.line > 1:     state.line   -= 1
        elif state.offset > 0: state.offset -= 1
        
        current_text = state.arr[state.line + state.offset - state.banoff]
        state.cursor = len(current_text)


def right(state):
    """Move cursor right one character"""
    current_text = state.arr[state.line + state.offset - state.banoff]
    
    if state.cursor < len(current_text):
        state.cursor += 1
        state.oldptr = state.cursor
    elif state.offset + state.line <= len(state.arr) - 1:
        # Move to beginning of next line
        if state.line > state.rows: state.offset += 1
        else:                       state.line   += 1
        state.cursor = 0


def backspace(state):
    """Delete character before cursor or merge lines"""
    current_text = state.arr[state.line + state.offset - state.banoff]
    
    if not state.select_mode or len(state.select) == 0:
        if state.cursor != 0:
            # Delete character before cursor
            text_chars = list(current_text) + [""]
            try:    text_chars.pop(state.cursor - 1)
            except: text_chars.pop(state.cursor)
            current_text = "".join(text_chars)
            state.cursor -= 1
        else:
            # Merge with previous line
            if state.offset + state.line != 1:
                previous_text = state.arr[state.line + state.offset - state.banoff - 1]
                state.arr[state.line + state.offset - state.banoff - 1] = previous_text + current_text
                state.arr.pop(state.line + state.offset - state.banoff)
                state.cursor = len(previous_text)
                current_text = previous_text + current_text
                
                if state.offset == 0: state.line -= 1
                else: state.offset -= 1
        
        state.arr[state.line + state.offset - state.banoff] = current_text
    else:
        # Delete selection
        del_sel(state)
        state.cursor = 0
        state.select_mode = False
        state.select = []
    state.status_st = False


def newline(state):
    """Insert newline at cursor position"""
    current_text = state.arr[state.line + state.offset - state.banoff]
    
    if not state.select_mode or len(state.select) == 0:
        # Split line at cursor
        before_cursor = current_text[:state.cursor]
        after_cursor = current_text[state.cursor:]
        
        state.arr[state.line + state.offset - state.banoff] = before_cursor
        state.arr.insert(state.line + state.offset - state.banoff + 1, after_cursor)
        
        # Move to new line
        if state.line < state.rows: state.line   += 1
        else:                       state.offset += 1
        state.cursor = 0
    else:
        # Replace selection with newline
        del_sel(state, True)
        state.cursor = 0
        state.select_mode = False
        state.select = []



def tab(state):
    """Insert tab or spaces at cursor position"""
    current_text = state.arr[state.line + state.offset - state.banoff]
    
    if not state.select_mode or len(state.select) == 0:
        # Insert tab/indent at cursor
        before_cursor = current_text[:state.cursor]
        after_cursor = current_text[state.cursor:]
        
        if state.indent == "tab":
            new_text = before_cursor + "\t" + after_cursor
            state.cursor += 1
        else:
            new_text = before_cursor + "    " + after_cursor
            state.cursor += 4
        
        state.arr[state.line + state.offset - state.banoff] = new_text
    else:
        # Indent selection
        start_line, start_offset = state.select[0]
        end_line, end_offset = state.select[1]
        
        for i in range(start_line + start_offset, end_line + end_offset + 1):
            if i < len(state.arr):
                if state.indent == "tab":
                    state.arr[i] = "\t" + state.arr[i]
                else:
                    state.arr[i] = "    " + state.arr[i]


