#Code by Sergio1260

from msvcrt import getch

def fixlenline(text, pointer, oldptr, p_offset):
    if p_offset+pointer>len(text)+2: p_offset=0
    length=len(text)+1
    if pointer>length or oldptr>length:
        return length,oldptr,p_offset
    elif oldptr>pointer: return oldptr,oldptr,p_offset
    else: return pointer,oldptr,p_offset

def supr(pointer, max_len, text, offset, banoff, arr, line, p_offset):
    if not pointer==max_len+1:
        p1=list(text); p1.pop(pointer+p_offset-1)
        text="".join(p1)
    elif not line+offset==1: #move all to previous line
        seltext=arr[line+offset-banoff+1]
        arr[line+offset-banoff+1]=text+seltext
        arr.pop(line+offset-banoff+1)
        text=text+seltext
    return text, arr

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
        if p_offset < 0: p_offset = 0
        if p_offset + columns > len(text): p_offset = len(text) - columns+1
        fix_text = text[p_offset:p_offset + columns]
        if p_offset > 0: fix_text=black+'<'+reset+fix_text[1:]
        if p_offset+columns<len(text): fix_text=fix_text[:-1]+black+'>'+reset
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

def left(pointer,oldptr,line,offset,banoff,columns,p_offset,text,arr):
    if not pointer==1: pointer-=1; oldptr=pointer
    elif not p_offset==0: p_offset-=1; oldptr=pointer
    elif not line+offset==1:
        if offset==0: line-=1
        else: offset-=1
        text=arr[line+offset-banoff]
        pointer=len(text)+1
        if pointer>columns+2:
            p_offset=len(text)-columns+2
            pointer=columns
    return pointer, oldptr, p_offset, text, line, offset

def right(pointer,p_offset,text,columns,offset,line,banoff,arr,rows,oldptr):
    if not pointer+p_offset>len(text):
        if not pointer>columns-1: pointer+=1
        else: p_offset+=1
        oldptr=pointer
    else:
        if not line==rows: line+=1
        else: offset+=1
        pointer=1; p_offset=0
        text=arr[line+offset-banoff]
    return text, pointer, p_offset, oldptr, line, offset

