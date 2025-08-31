# Code by Sergio00166

from os import sep, read

# BOM (Byte Order Mark) mappings for different encodings
BOM_MAP = {
    b"\xef\xbb\xbf": "utf-8-sig",
    b"\xff\xfe": "utf-16-le",
    b"\xfe\xff": "utf-16-be",
}
REV_BOM_MAP = {
    "utf-8-sig": b"\xef\xbb\xbf",
    "utf-16-le": b"\xff\xfe",
    "utf-16-be": b"\xfe\xff",
}
CODECS_NO_BOM = ("utf-8", "utf-16", "latin_1")


def calc_displacement(state, data, rect=0):
    """Update state.line and state.offset after inserting data"""
    state.line += len(data) - rect

    overflow = state.line - state.banoff - state.rows
    if overflow > 0:
        state.offset += overflow
        state.line = state.rows + state.banoff


def calc_rel_line(state, target_line):
    """Calculate relative line position"""
    if target_line == "-": 
        target_line = len(state.arr) - 1
    else:
        try: target_line = int(target_line)
        except: return

    if target_line >= len(state.arr): return 

    part = state.rows // 2
    new_offset = target_line - part
    new_line = part if new_offset >= 0 else target_line
    state.line = new_line + state.banoff
    state.offset = max(new_offset, 0)


# Detect if indent is tab or space
def taborspace(contents):
    sp_cnt, tab_cnt = 0, 0
    for x in contents:
        if x.startswith(" " * 4):
            sp_cnt += 1
        if x.startswith("\t"):
            tab_cnt += 1
    return " " * 4 if sp_cnt > tab_cnt else "\t"


def detect_line_ending_char(c):
    c = c[:1024]
    crlf = c.count("\r\n")
    c = c.replace("\r\n", "")
    cr = c.count("\r")
    lf = c.count("\n")
    if crlf > cr and crlf > lf:
        return "\r\n"
    elif cr > lf:
        return "\r"
    else:
        return "\n"


def read_UTF8(path):
    data, codec = open(path, "rb").read(), None

    for bom, encoding in BOM_MAP.items():
        if data.startswith(bom):
            data, codec = data[len(bom) :], encoding
            break
    if codec:
        data = data.decode(codec)
        lnsep = detect_line_ending_char(data)
        data = data.split(lnsep)
        return data, codec, lnsep

    for codec in CODECS_NO_BOM:
        try:
            data = data.decode(codec)
            lnsep = detect_line_ending_char(data)
            data = data.split(lnsep)
            return data, codec, lnsep
        except: pass

    raise UnicodeError


def write_UTF8(path, codec, lnsep, data):
    file = open(path, "wb")
    data = lnsep.join(data).encode(codec)
    if codec in REV_BOM_MAP:
        bom = REV_BOM_MAP[codec]
        data = bom + data
    file.write(data)
    file.close()


