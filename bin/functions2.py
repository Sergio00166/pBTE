#Code by Sergio1260


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
