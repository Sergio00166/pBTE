#Code by Sergio1260

from special_keys import special_keys
from functions import *
from actions import *
from saveas import save_as
from openfile import open_file

def keys(key,text,pointer,oldptr,line,offset,columns,banoff,arr,rows,\
         max_len,filename,status,status_st,copy_buffer,fixstr,fix,\
         black,reset,saved_txt,ch_T_SP,banner):
        
    if key==b'\xe0': #Special Keys
        text, pointer, oldptr, line, offset, status_st =\
        special_keys(pointer,text,columns,offset,line,banoff,\
                     arr,rows,oldptr,max_len,status_st)
        
    elif key==b'\x08': #Backspace (removes char)
        line, offset, text, arr, pointer =\
        backspace(pointer,text,offset,line,arr,banoff)
        status_st=False

    elif key==b'\r': #Return (adds new lines or moves text)
        line, offset, arr, pointer, text =\
        newline(text,pointer,offset,banoff,line,arr,rows)
        status_st=False

    elif key==b'\x13': #Ctrl + S (SAVE)
        out=open(filename,"w",encoding="UTF-8")
        out.write("\n".join(arr)); out.close()
        status=saved_txt; status_st=True
        out=open(filename,"r",encoding="UTF-8")
        
    elif key==b'\x18': #Ctrl + X (CUT LINE)
        if line+offset>len(arr)-1:
            copy_buffer=text[pointer-1:]
            text=text[:pointer-1]
        else:
            copy_buffer=arr[line+offset-banoff]
            arr.pop(line+offset-banoff)
            text=arr[line+offset-banoff]
        status_st=False
        
    elif key==b'\x03': #Ctrl + C (COPY LINE)
        copy_buffer=arr[line+offset-banoff][pointer-1:]
        
    elif key==b'\x10': #Ctrl + P (PASTE TEXT)
        if not len(copy_buffer)==0:
            p1=arr[:line+offset-banoff]; p2=arr[line+offset-banoff+1:]
            fix1=text[:pointer-1]; fix2=text[+pointer-1:]
            out=fix1+copy_buffer+fix2; arr=p1+[out]+p2; text=out
            pointer=len(fix1+copy_buffer)
            status_st=False

    elif key==b'\x07': #Ctrl + G (go to line)
        line,offset,text = goto(rows,banoff,line,arr,offset,black,reset)

    elif key==b'\x01': #Ctrl + A (Save as)
        args=(filename,black,reset,rows,banoff,arr,columns,\
        status,offset,line,banner,status_st,saved_txt)
        status_st, filename, status = save_as(args)

    elif key==b'\x0f': #Ctlr + O (Open file)
        args=(filename,black,reset,rows,banoff,arr,columns,status,offset,line,banner,status_st)
        arr,filename,status_st = open_file(args); line=1; offset=0; text=arr[0]

    elif key==b'\x14': #Ctrl + T (Use 4 spaces instead of tabs)
        if ch_T_SP: ch_T_SP=False
        else: ch_T_SP=True

    elif key==b'\n': pass
        
    else: #All the other keys
        if not str(key)[4:6] in fixstr:
            out=decode(key)
            p1=text[:pointer-1]
            p2=text[pointer-1:]
            if out=="\t" and ch_T_SP:
                out=" "*4
                pointer+=3
            text=(p1+out+p2)
            pointer+=1
            status_st=False

    return text,pointer,oldptr,line,offset,columns,banoff,arr,rows,max_len,filename,status,status_st,copy_buffer,fixstr,fix,ch_T_SP

