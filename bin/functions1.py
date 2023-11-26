#Code by Sergio1260

from fixes import *

def supr(pointer,max_len,text,offset,banoff,arr,line,p_offset,tabchr,tab_len):
    if not pointer+p_offset==len(text)+1 and text[pointer+p_offset-1]==tabchr:
        p1=text[:pointer+p_offset-1]
        p2=text[pointer+p_offset-1:]
        for x in range(tab_len):
            if not len(p2)==0 and p2[0]==tabchr:
                p2=p2[1:]
        text=(p1+p2)
    
    elif not pointer==max_len+1:
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

def backspace(pointer,text,offset,line,arr,banoff,p_offset,tabchr,tab_len):
    if not pointer==1: #Delete char
        if text[pointer+p_offset-2]==tabchr:
            p1=text[:pointer+p_offset-1]
            p2=text[pointer+p_offset-1:]
            for x in range(tab_len):
                if not len(p1)==0 and p1[len(p1)-1]==tabchr:
                    p1=p1[:-1]
                    if p_offset==0: pointer-=1
                    else: p_offset-=1
            text=(p1+p2)
        else:   
            p1=list(text)+[""]
            if p_offset>0: fix=1
            else: fix=0
            p1.pop(pointer+p_offset-2-fix)
            text="".join(p1)
            if p_offset==0: pointer-=1
            else: p_offset-=1
    else: #move all to previous line
        if not offset+line==1:
            seltext=arr[line+offset-banoff-1]
            arr[line+offset-banoff-1]=seltext+text
            arr.pop(line+offset-banoff)
            pointer=len(seltext)+1
            text=seltext+text
            if not offset==0: offset-=1
            else: line-=1
    return line, offset, text, arr, pointer, p_offset
