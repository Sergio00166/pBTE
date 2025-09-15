# Code by Sergio00166


def cmt_w_ind(string, sepstr):
    """Extract indentation and content from string"""
    pos, length = 0, len(sepstr)
    while string.startswith(sepstr, pos):
        pos += length
    return string[:pos], string[pos:]


def del_sel(state, blank=False):
    """Delete selected text in-place using state"""
    start_pos = sum(state.select[0])
    end_pos = sum(state.select[1])

    # Split array around selection
    before_selection = state.arr[:start_pos]
    after_selection = state.arr[end_pos:]

    # Mutate state.arr in-place
    state.arr = before_selection + ([""] if blank else []) + after_selection

    # Base values
    line   = state.select[0][0] + state.banoff
    offset = state.select[0][1]

    # Break condition into parts
    past_bottom = line + offset - state.banoff > len(state.arr) - 1
    too_low     = line > state.banoff and past_bottom

    # Update values
    state.line   = line   - (too_low and offset == 0)
    state.offset = offset - (too_low and offset > 0)
    state.select = []


def select_add_start_str(state, text, remove=False):
    # Calculate selection bounds
    start = sum(state.select[0])
    end = sum(state.select[1])
    # Slice the selected region
    p1 = state.arr[start:end]

    # Apply formatting or removal
    if isinstance(text, list):
        if not remove:
            state.arr[start:end] = [text[0] + x + text[1] for x in p1]
        else:
            state.arr[start:end] = [
                x[len(text[0]):] if len(text[1]) == 0 and x.startswith(text[0])
                else (
                    x[len(text[0]):-len(text[1])]
                    if x.startswith(text[0]) and x.endswith(text[1])
                    else x
                )
                for x in p1
            ]
    elif not remove:
        state.arr[start:end] = [text + x for x in p1]
    else:
        state.arr[start:end] = [x[len(text):] if x.startswith(text) else x for x in p1]



def search_substring(lst, substring, start_list_pos=0, start_string_pos=0):
    list_lenght, i = len(lst), start_list_pos
    while True:
        start = start_string_pos if i == start_list_pos else 0
        for j in range(start, len(lst[i])):
            if lst[i][j : j + len(substring)] == substring:
                return i, j + len(substring)
        i, start_string_pos = (i + 1) % list_lenght, 0


def search_substring_rev(lst, substring, start_list_pos=0, start_string_pos=None):
    list_lenght, i = len(lst), start_list_pos
    while True:
        start = start_string_pos if i == start_list_pos else len(lst[i])
        if start_string_pos is None:
            start = len(lst[i])
        else:
            start = start_string_pos - len(find_str)
        for j in range(start, -1, -1):
            if lst[i][j - len(substring) : j] == substring:
                return i, j
        i, start_string_pos = (i - 1) % list_lenght, None




