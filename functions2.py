#Code by Sergio1260

def decode(key):
    for x in range(3):
        try: out=key.decode("UTF-8"); break
        except: key+=getch()
    return out

def fixlenline(text, pointer, oldptr, p_offset):
    if p_offset+pointer>len(text)+2: p_offset=0
    length=len(text)
    if pointer>length or oldptr>length:
        return length,oldptr,p_offset
    elif oldptr>pointer: return oldptr,oldptr,p_offset
    else: return pointer,oldptr,p_offset

def down(line, offset, arr, text, banoff, oldptr, rows, pointer, p_offset):
    if not line+offset==len(arr)+banoff-1:
        if not line==rows+banoff: line+=1
        elif not line+offset==len(arr)+1: offset+=1
        text=arr[line+offset-banoff]
        pointer,oldptr,p_offset=fixlenline(text,pointer,oldptr,p_offset)
    return pointer, oldptr, text, offset, line, p_offset

def up(line, offset, arr, text, banoff, oldptr, rows, pointer, p_offset):
    if not line==banoff: line-=1
    elif offset>0: offset-=1
    text=arr[line+offset-banoff]
    pointer,oldptr,p_offset=fixlenline(text,pointer,oldptr,p_offset) 
    return pointer, oldptr, text, offset, line, p_offset

def fix_line(text, p_offset, black, reset, columns):
    if len(text)>columns:
        if p_offset < 0:
            p_offset = 0
        if p_offset + columns > len(text):
            p_offset = len(text) - columns+1
        fix_text = text[p_offset:p_offset + columns]

        if p_offset > 0:
            fix_text=black+'<'+reset+fix_text[1:]
        if p_offset+columns<len(text):
            fix_text=fix_text[:-1]+black+'>'+reset
    else: fix_text=text
    return fix_text

def fix_scr(arr, org_arr, p_offset, black, reset, columns, line, offset, banoff):
    out=[]
    for x in arr: out.append(fix_line(x, 0, black, reset, columns))
    x=org_arr[line+offset-banoff]
    try:
        out[line-banoff]=fix_line(x, p_offset, black, reset, columns)
        return "\n".join(out)
    except:
        out.append(fix_line(x, p_offset, black, reset, columns))
        return "\n".join(out[1:])
    
    
        
