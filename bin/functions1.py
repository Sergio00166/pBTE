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

def newline(text, pointer, offset, banoff, line, arr, rows):
    p1=arr[:line+offset-banoff]
    p2=arr[line+offset-banoff:]
    if not len(text)==0:
        fix=1
        seltext=[text[:pointer-fix]]
        arr=p1+seltext+p2
        text=text[pointer-fix:]
        pointer=0
    else: arr=p1+[""]+p2
    if not line>rows: line+=1
    else: offset+=1
    return line, offset, arr, pointer, text


def left(pointer,oldptr,line,offset,banoff,text,arr):
    if not pointer==1: pointer-=1; oldptr=pointer
    elif not line+offset==1:
        if offset==0: line-=1
        else: offset-=1
        text=arr[line+offset-banoff]
        pointer=len(text)+1
    return pointer, oldptr, text, line, offset

def right(pointer,text,columns,offset,line,banoff,arr,rows,oldptr):
    if not pointer>len(text):
        pointer+=1
        oldptr=pointer
    else:
        if not offset+line>len(arr)-1:
            if not line>rows-2: line+=1
            else: offset+=1
            pointer=1
            text=arr[line+offset-banoff]
    return text, pointer, oldptr, line, offset

def goto(rows, banoff, line, arr, offset, black, reset):
    print("\r\033[%d;%dH"%(rows+banoff+2,1),end="")
    print(" "+black+"Go to line:"+reset, end=" "); p1=input()
    print("\r\033[%d;%dH"%(line, 1),end="")
    if p1=="-": p1=len(arr)-1
    try:
        p1=int(p1)
        if p1<len(arr):
            if p1<rows: offset=0; line=p1+banoff
            else: offset=p1-rows; line=rows+banoff
        text=arr[line+offset-banoff]
    except: pass
    return line, offset, text

