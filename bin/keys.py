#Code by Sergio1260

from special_keys import special_keys
from fixes import *
from functions1 import *
from functions2 import *
from saveas import save_as
from openfile import open_file

def keys(key,text,pointer,p_offset,oldptr,line,offset,columns,banoff,arr,rows,max_len,filename,\
         status,status_st,copy_buffer,fixstr,fix,black,reset,saved_txt,tab_len,tabchr,ch_T_SP):
        
    if key==b'\xe0': #Special Keys
        text, pointer, p_offset, oldptr, line, offset, status_st =\
        special_keys(pointer,p_offset,text,columns,offset,line,banoff,\
                     arr,rows,oldptr,max_len,status_st,tabchr,tab_len)
        
    elif key==b'\x08': #Backspace (removes char)
        line, offset, text, arr, pointer, p_offset =\
        backspace(pointer,text,offset,line,arr,banoff,p_offset,tabchr,tab_len)
        status_st=False

    elif key==b'\r': #Return (adds new lines or moves text)
        line, offset, arr, pointer, text =\
        newline(text,pointer,offset,banoff,line,arr,rows,p_offset)
        status_st=False

    elif key==b'\x13': #Ctrl + S (SAVE)
        out=open(filename,"w",encoding="UTF-8")
        arr1=fix_out_tab(arr,tabchr,tab_len)
        out.write("\n".join(arr1)); out.close()
        status=saved_txt; status_st=True
        out=open(filename,"r",encoding="UTF-8")
        arr=out.readlines()+[""]
        arr=fix_read_tab(arr,tab_len,tabchr)
        
    elif key==b'\x18': #Ctrl + X (CUT LINE)
        if not line+offset>len(arr)-1:
            copy_buffer=arr[line+offset-banoff][pointer+p_offset-1:]
            arr.pop(line+offset-banoff); text=arr[line+offset-banoff]
            status_st=False
        
    elif key==b'\x03': #Ctrl + C (COPY LINE)
        copy_buffer=arr[line+offset-banoff][pointer+p_offset-1:]
        
    elif key==b'\x10': #Ctrl + P (PASTE TEXT)
        if not len(copy_buffer)==0:
            p1=arr[:line+offset-banoff]; p2=arr[line+offset-banoff+1:]
            fix1=text[:p_offset+pointer-1]; fix2=text[p_offset+pointer-1:]
            out=fix1+copy_buffer+fix2; arr=p1+[out]+p2; text=out
            status_st=False

    elif key==b'\x07': #Ctrl + G (go to line)
        line,offset,text = goto(rows,banoff,line,arr,offset,black,reset)

    elif key==b'\x01': #Ctrl + A (Save as)
        arr, status_st, filename, status =\
        save_as(filename,black,reset,rows,banoff,arr,saved_txt,\
                status_st,columns,status,tabchr,tab_len)

    elif key==b'\x0f': #Ctlr + O (Open file)
        arr,filename = open_file(filename,black,\
        reset,rows,banoff,arr,columns,tab_len,tabchr)
        text=arr[0]

    elif key==b'\x14': #Ctrl + T (Use 4 spaces instead of tabs)
        if ch_T_SP: ch_T_SP=False
        else: ch_T_SP=True
        
    else: #All the other keys
        if not str(key)[4:6] in fixstr:
            out=decode(key)
            p1=text[:pointer+p_offset-1]
            p2=text[pointer+p_offset-1:]
            if key==b'\t': #Tab fix
                if p2=="": p2=tabchr; fix_empty=1
                else: fix_empty=0
                text=(p1+out+p2)    
                #Set spaces as 4 for python
                if ch_T_SP: tabchr=" "; fix=4
                else: fix=fix_tab(pointer+p_offset,text,tab_len)
                out=tabchr*(fix-fix_empty)
            else: fix=1;
            text=(p1+out+p2)
            if p_offset==0 and not pointer+fix>columns: pointer+=fix
            elif not p_offset+pointer>len(text)+2: p_offset+=fix
            else: pointer+=fix
            status_st=False

    return text,pointer,p_offset,oldptr,line,offset,columns,banoff,arr,rows,max_len,filename,status,status_st,copy_buffer,fixstr,fix,ch_T_SP

