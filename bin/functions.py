#Code by Sergio1260

from os import get_terminal_size,sep
from sys import path
path.append(path[0]+sep+"lib.zip")
from wcwidth import wcwidth


def wrap(text, columns):
    text=text.expandtabs(8)
    out=[]; counter=-1; buffer=""
    for x in text:
        if counter>=columns-1:
            lenght=str_len(x)
            if lenght>1: ext=buffer; buffer=x
            else: ext=buffer+x; buffer=""    
            out.append(ext); counter=0
        else: buffer+=x; counter+=str_len(x)
    if not buffer=="": out.append(buffer)
    return out

def get_size():
    size=get_terminal_size()
    return size[1]-3,size[0]-2

def decode(key,getch):
    for x in range(3):
        try: out=key.decode("UTF-8"); break
        except: key+=getch()
    return out

def fix_arr_line_len(arr, columns, black, reset):
    out=[]; fix=0//(columns+2)
    for text in arr:
        wrapped_text = wrap(text,columns)
        if len(wrapped_text)==0: wrapped_text=""
        elif fix==len(wrapped_text):
            text=wrapped_text[fix-1]
        else: text=wrapped_text[fix]
        if (len(wrapped_text)-fix)>1:
            text+=black+">"+reset
        out.append(text)   
    return out

def str_len(text,pointer=None):
    lenght=0
    if not pointer==None:
        fix=text[:pointer-1]
    else: fix=text
    fix=fix.expandtabs(8)
    for x in fix: lenght+=wcwidth(x)
    return lenght

def fixlenline(text, pointer, oldptr):
    length=len(text)+1
    if pointer>length or oldptr>length:
        return length,oldptr
    elif oldptr>pointer: return oldptr,oldptr
    else: return pointer,oldptr

def CalcRelLine(p1,arr,offset,line,banoff,rows):
    if p1=="-": p1=len(arr)-1
    try:
        p1=int(p1)
        if p1<len(arr):
            if p1<rows: offset=0; line=p1+banoff
            else: offset=p1-rows; line=rows+banoff
    except: pass
    text=arr[line+offset-banoff]
    return line, offset, text

def fix_cursor_pos(text,pointer,columns,black,reset):
    len_arr=[]; ptr=pointer; pos=0
    pointer=str_len(text,pointer)   
    fix=pointer//(columns+2)
    wrapped_text = wrap(text,columns)  
    for x in wrapped_text:
        if pointer-str_len(x)<1: break
        else: pos+=1
        pointer-=str_len(x)
    if pos>0: pointer+=1
    if len(wrapped_text)==0: wrapped_text==""
    else: text=wrapped_text[pos]
    if fix>0: text=black+"<"+reset+text
    if (len(wrapped_text)-fix)>1: text+=black+">"+reset
    return pointer+1, text

def update_scr(black,reset,status,banoff,offset,line,pointer,arr,banner,filename,rows,columns):
    position=black+"  "+str(line+offset-banoff)+" "*(4-len(str(line+offset-banoff)))
    text=arr[line+offset-1]; pointer, text = fix_cursor_pos(text,pointer,columns,black,reset)
    out_arr=fix_arr_line_len(arr[offset:rows+offset+1], columns, black, reset)
    cls="\r\033[%d;%dH"%(1, 1)+(" "*(columns+2))*(rows+2)+"\r\033[%d;%dH"%(1, 1)
    out_arr[line-1]=text 
    all_file="\n".join(out_arr).expandtabs(8)
    outb=position+black+" "+reset+status+banner
    outb=outb+black+"    "+reset
    if len(filename)+31>columns: #If filename overflows
        flfix=filename.split(sep)
        filename=flfix[len(flfix)-1]
        if len(filename)+31>columns: #If still not fiting
            middle = len(filename) // 2
            filename=filename[:middle-1]+'*'+filename[middle+2:]    
    print(cls+outb+black+" "*(columns-31-len(filename))+reset, end="")
    print(black+filename+reset+black+" "+reset+"\n"+all_file, end="")
    print(("\r\033[%d;%dH"%(line+1, pointer)), end="")
