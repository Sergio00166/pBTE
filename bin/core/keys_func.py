# Code by Sergio00166

from functions import write_UTF8, calc_rel_line
from text_op import cmt_w_ind, select_add_start_str
from inputs import decode, handle_text_input
from scr_utils import str_len
from actions import *
from actions1 import *
from saveas import save_as
from openfile import open_file
from find_str import find
from replace_str import replace
from chg_var_str import chg_var_str
from opt_menu import opt_menu


def keys_func(state, key):
    """Process key input and execute corresponding actions"""

    action_map = {
        state.keys["ctrl+x"]: cut,
        state.keys["ctrl+c"]: copy,
        state.keys["ctrl+p"]: paste,
        state.keys["delete"]: backspace,
        state.keys["supr"]:   supr,
        state.keys["return"]: newline,
        state.keys["ctrl+a"]: save_as,
        state.keys["ctrl+o"]: open_file,
        state.keys["ctrl+f"]: find,
        state.keys["ctrl+r"]: replace,
        state.keys["ctrl+k"]: comment_func,
        state.keys["ctrl+u"]: uncomment_func,
        state.keys["ctrl+t"]: opt_menu
    }   
    if key in action_map: action_map[key](state)

    # Toggle selection mode
    elif key == state.keys["ctrl+y"]:
        state.select_mode = not state.select_mode
        if not state.select_mode:
            state.select = []
    
    # Move up (with optional Ctrl for faster movement)
    elif key in (state.keys["arr_up"], state.keys["ctrl+arr_up"]):
        times = 4 if key == state.keys["ctrl+arr_up"] else 1
        for _ in range(times): up(state)
    
    # Move down (with optional Ctrl for faster movement)
    elif key in (state.keys["arr_down"], state.keys["ctrl+arr_down"]):
        times = 4 if key == state.keys["ctrl+arr_down"] else 1
        for _ in range(times): down(state)
    
    # Move right (with optional Ctrl for faster movement)
    elif key in (state.keys["arr_right"], state.keys["ctrl+arr_right"]):
        times = 4 if key == state.keys["ctrl+arr_right"] else 1
        for _ in range(times): right(state)
        state.select = []
    
    # Move left (with optional Ctrl for faster movement)
    elif key in (state.keys["arr_left"], state.keys["ctrl+arr_left"]):
        times = 4 if key == state.keys["ctrl+arr_left"] else 1
        for _ in range(times): left(state)
        state.select = []
    
    # Go to start of line
    elif key in state.keys["start"]:
        state.cursor, state.oldptr, state.select = 0, 0, []
    
    # Go to end of line
    elif key in state.keys["end"]:
        current_text = state.arr[state.line + state.offset - state.banoff]
        state.cursor = len(current_text)
        state.oldptr, state.select = state.cursor, []
    
    # Page up
    elif key == state.keys["repag"]:
        for _ in range(state.rows): up(state)
    
    # Page down
    elif key == state.keys["avpag"]:
        for _ in range(state.rows): down(state)

    # Save file
    elif key == state.keys["ctrl+s"]:
        try:
            write_UTF8(state,state.filename)
            state.status = "SAVED"
        except:
            state.status = "ERROR"
        state.status_st = True

    # Go to line
    elif key == state.keys["ctrl+g"]:
        user_input = chg_var_str(state, "", " Go to: ")
        if user_input == "-":
            target_line = len(state.arr) - 1
        elif user_input.isdigit():
            target_line = int(user_input)
        else:
            target_line = state.line + state.offset - state.banoff
        
        calc_rel_line(state, target_line)
    
    # Insert character (for regular text input)
    else: handle_text_input(state, key)

