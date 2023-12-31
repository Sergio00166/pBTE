#Code by Sergio1260

from sys import path
path.append(path[0]+"\\lib.zip")
from wcwidth import wcwidth
from functions import wrap, str_len, tab_len, fix_arr_line_len


def fix_cursor_pos(text,pointer,columns,black,reset):
    
    len_arr=[]; ptr=pointer
    pointer=str_len(text,pointer)
    
    fix=pointer//(columns+2)
    wrapped_text = wrap(text,columns)
    if len(wrapped_text)==0: wrapped_text=""
    elif fix==len(wrapped_text):
        text=wrapped_text[fix-1]
    else: text=wrapped_text[fix]
    pointer-=(fix*columns)
    if fix>0: text=black+"<"+reset+text
    if (len(wrapped_text)-fix)>1:
        text+=black+">"+reset

    return pointer+1, text

def update_scr(black,reset,legacy,status,banoff,offset,line,pointer,arr,banner,filename,rows,columns):
    
    position=black+"  "+str(line+offset-banoff)+" "*(4-len(str(line+offset-banoff)))
    text=arr[line+offset-1]
    pointer, text = fix_cursor_pos(text,pointer,columns,black,reset)
    out_arr=arr[offset:rows+offset+1]
    out_arr=fix_arr_line_len(out_arr, columns, black, reset)
    out_arr[line-1]=text
    all_file="\n".join(out_arr).expandtabs(8)
    outb=position+black+" "+reset+status+banner
    outb=outb+black+"    "+reset
    
    if not legacy: cls="\033c"
    else: cls=("\r\033[%d;%dH"%(rows+3, columns+2))+"\n"
    fix=("\r\033[%d;%dH"%(1, 1))
    
    if len(filename)+31>columns: #If filename overflows
        flfix=filename.split("\\")
        filename=flfix[len(flfix)-1]
        if len(filename)+31>columns: #If still not fiting
            filename=filename[:5]+"*"+filename[len(filename)-4:]
            
    print(cls+outb+black+" "*(columns-31-len(filename))+reset, end="")
    print(black+filename+reset+black+" "+reset+"\n"+all_file, end="")
    print(("\r\033[%d;%dH"%(line+1, pointer)), end="")


