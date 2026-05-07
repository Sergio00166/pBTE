# Code by Sergio00166

from text_op import cmt_w_ind, select_add_start_str
from functions import write_UTF8, calc_rel_line
from inputs import decode, handle_text_input
from data import keys, keys_raw
from scr_utils import str_len

from chg_var_str import chg_var_str
from replace_str import replace
from openfile import open_file
from opt_menu import opt_menu
from saveas import save_as
from find_str import find
from actions1 import *
from actions import *


def keys_func(state, kbd_input):
    action_map = {
        keys["tab"]: indent,
        keys["ctrl+x"]: cut,
        keys["ctrl+c"]: copy,
        keys["ctrl+p"]: paste,
        keys["delete"]: supr,
        keys["return"]: newline,
        keys["ctrl+a"]: save_as,
        keys["ctrl+o"]: open_file,
        keys["ctrl+f"]: find,
        keys["ctrl+r"]: replace,
        keys["ctrl+d"]: dedent,
        keys["ctrl+k"]: comment_func,
        keys["ctrl+u"]: uncomment_func,
        keys["ctrl+t"]: opt_menu,
        keys["backspace"]: backspace
    }   
    if kbd_input in action_map: action_map[kbd_input](state)

    elif kbd_input == keys["ctrl+y"]:
        state.select_mode = not state.select_mode
        if not state.select_mode:
            state.select = []

    elif kbd_input in (keys["arr_up"], keys["ctrl+arr_up"]):
        times = 4 if kbd_input == keys["ctrl+arr_up"] else 1
        for _ in range(times): up(state)

    elif kbd_input in (keys["arr_down"], keys["ctrl+arr_down"]):
        times = 4 if kbd_input == keys["ctrl+arr_down"] else 1
        for _ in range(times): down(state)

    elif kbd_input in (keys["arr_right"], keys["ctrl+arr_right"]):
        times = 4 if kbd_input == keys["ctrl+arr_right"] else 1
        for _ in range(times): right(state)
        state.select = []

    elif kbd_input in (keys["arr_left"], keys["ctrl+arr_left"]):
        times = 4 if kbd_input == keys["ctrl+arr_left"] else 1
        for _ in range(times): left(state)
        state.select = []

    elif kbd_input in keys["start"]:
        state.cursor, state.oldptr, state.select = 0, 0, []

    elif kbd_input in keys["end"]:
        current_text = state.arr[state.line + state.offset - state.banoff]
        state.cursor = len(current_text)
        state.oldptr, state.select = state.cursor, []

    elif kbd_input == keys["pageup"]:
        for _ in range(state.rows): up(state)

    elif kbd_input == keys["pagedown"]:
        for _ in range(state.rows): down(state)

    elif kbd_input == keys["ctrl+s"]:
        try:
            write_UTF8(state)
            state.status = "SAVED"
        except:
            state.status = "ERROR"
        state.status_st = True

    elif kbd_input == keys["ctrl+g"]:
        user_input = chg_var_str(state, "", " Go to: ")

        if user_input == "-":
            target_line = len(state.arr) - 1

        elif user_input.isdigit():
            target_line = int(user_input)

        else:
            target_line = state.line + state.offset - state.banoff

        calc_rel_line(state, target_line)

    elif kbd_input in keys_raw: return
    else: handle_text_input(state, kbd_input)


 