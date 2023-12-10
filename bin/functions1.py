#Code by Sergio1260

from functions import *

def supr(pointer,max_len,text,offset,banoff,arr,line):
    if not pointer==max_len+1:
        p1=list(text); p1.pop(pointer-1)
        text="".join(p1)
    elif not line+offset==1: #move all to previous line
        seltext=arr[line+offset-banoff+1]
        arr[line+offset-banoff+1]=text+seltext
        arr.pop(line+offset-banoff+1)
        text=text+seltext
    return text, arr

def down(line, offset, arr, text, banoff, oldptr, rows, pointer):
    if not line+offset==len(arr)+banoff-1:
        if not line==rows+banoff: line+=1
        elif not line+offset==len(arr)+1: offset+=1
        text=arr[line+offset-banoff]
        pointer,oldptrt=fixlenline(text,pointer,oldptr)
    return pointer, oldptr, text, offset, line

def up(line, offset, arr, text, banoff, oldptr, rows, pointer):
    if not line==banoff: line-=1
    elif offset>0: offset-=1
    text=arr[line+offset-banoff]
    pointer,oldptr=fixlenline(text,pointer,oldptr) 
    return pointer, oldptr, text, offset, line

def backspace(pointer,text,offset,line,arr,banoff):
    if not pointer==1: #Delete char   
        p1=list(text)+[""]
        p1.pop(pointer-2)
        text="".join(p1)
        pointer-=1
        
    else: #move all to previous line
        if not offset+line==1:
            seltext=arr[line+offset-banoff-1]
            arr[line+offset-banoff-1]=seltext+text
            arr.pop(line+offset-banoff)
            pointer=len(seltext)+1
            text=seltext+text
            if not offset==0: offset-=1
            else: line-=1
    return line, offset, text, arr, pointer
