#Code by Sergio1260


def newline(text, pointer, offset, banoff, line, arr, rows, p_offset):
    p1=arr[:line+offset-banoff]
    p2=arr[line+offset-banoff:]
    if not len(text)==0:
        if p_offset>0: fix=2
        else: fix=1
        seltext=[text[:pointer+p_offset-fix]]
        arr=p1+seltext+p2
        text=text[pointer+p_offset-fix:]
        pointer=0
    else: arr=p1+[""]+p2
    if not line>rows: line+=1
    else: offset+=1
    return line, offset, arr, pointer, text


def left(pointer,oldptr,line,offset,banoff,columns,p_offset,text,arr,tabchr,tab_len):
    if not pointer+p_offset==1 and text[pointer+p_offset-2]==tabchr:
        p1=text[:pointer+p_offset-1]
        for x in range(tab_len):
            if not len(p1)==0 and p1[len(p1)-1]==tabchr:
                p1=p1[:-1]
                if p_offset==0: pointer-=1
                else: p_offset-=1
        pointer+=1
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

def right(pointer,p_offset,text,columns,offset,line,banoff,arr,rows,oldptr,tabchr,tab_len):
    if not pointer+p_offset==len(text)+1 and text[pointer+p_offset-1]==tabchr:
        p1=text[pointer+p_offset-1:]
        for x in range(tab_len):
            if not len(p1)==0 and p1[0]==tabchr:
                p1=p1[1:]
                if p_offset==0: pointer+=1
                else: p_offset+=1

    elif not pointer+p_offset>len(text):
        if not pointer>columns-1: pointer+=1
        else: p_offset+=1
        oldptr=pointer
    else:
        if not offset+line>len(arr)-1:
            if not line>rows-2: line+=1
            else: offset+=1
            pointer=1; p_offset=0
            text=arr[line+offset-banoff]
    return text, pointer, p_offset, oldptr, line, offset

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
