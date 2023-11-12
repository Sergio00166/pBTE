#Code by Sergio1260

from msvcrt import getch

def delete(pointer, text, offset, line, arr, banoff, p_offset):
    if not pointer==1: #Delete char
        p1=list(text)+[""]
        if p_offset>0: fix=1
        else: fix=0
        p1.pop(pointer+p_offset-2-fix)
        text="".join(p1);
        if p_offset==0: pointer-=1
        else: p_offset-=1
    else: #move all to previous line
        if not offset+line==1:
            seltext=arr[line+offset-banoff-1]
            arr[line+offset-banoff-1]=seltext+text
            arr.pop(line+offset-banoff)
            pointer=len(seltext)+1
            text=seltext+text
            if not offset==0:
                offset-=1
            else: line-=1
    return line, offset, text, arr, pointer, p_offset

def goto(rows, banoff, line, arr, offset, black, reset):
    print("\r\033[%d;%dH"%(rows+banoff+2,1),end="")
    print(" "+black+"Go to line:"+reset, end=" "); p1=input()
    print("\r\033[%d;%dH"%(line, 1),end="")
    try:
        p1=int(p1)
        if p1<len(arr):
            if p1<rows:
                offset=0
                line=p1+banoff
            else:
                offset=p1-rows
                line=rows+banoff
    except: pass
    return line, offset

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

def newline(text, pointer, offset, banoff, line, arr, rows):
    seltext=[text[:pointer-1]]
    p1=arr[:line+offset-banoff]
    p2=arr[line+offset-banoff:]
    if not len(text)==0:
        seltext=[text[:pointer-1]]
        arr=p1+seltext+p2
        text=text[pointer-1:]
        pointer=0
    else: arr=p1+[""]+p2
    if not line>rows+1: line+=1
    else: offset+=1
    return line, offset, arr, pointer, text

def save_as(filename, black, reset, rows, banoff, arr, saved_txt):
    saveastxt=black+" Save as:"+reset+" "
    lenght=len(saveastxt)-16
    filewrite=filename
    wrtptr=lenght+len(filewrite)
    while True:
        print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
        print("\r"+" "*(len(filewrite)+lenght+1), end="")
        print("\r "+saveastxt+filewrite,end="")
        print("\r\033[%d;%dH"%(rows+banoff+2, wrtptr),end="")
        key=getch() #Map keys
        if key==b'\x13': #Ctrl + S (confirms)
            try:
                out=open(filewrite,"w",encoding="UTF-8")
                out.write("\n".join(arr)); out.close(); status=saved_txt; status_st=2
                status_st=2; tmp=open(filewrite, "r", encoding="UTF-8").readlines(); arr=[]
                for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
                arr.append(""); break
            except: pass

        elif key==b'\x11': #Ctrl + Q (cancel)
            break
    
        elif key==b'\x08': #Delete
            if not wrtptr==lenght:
                p1=list(filewrite); p1.pop(wrtptr-lenght-1)
                filewrite="".join(p1); wrtptr-=1

        elif key==b'\xe0': #Arrows
            arrow=getch()
            if arrow==b'K': #Left
                if not wrtptr==lenght:
                    wrtptr-=1
            elif arrow==b'M': #Right
                if not wrtptr>len(filewrite)+lenght-1:
                    wrtptr+=1

        else: #Rest of keys
            out=decode(key)
            p1=filewrite[:wrtptr-lenght]
            p2=filewrite[wrtptr-lenght:]
            filewrite=p1+out+p2
            wrtptr+=1

    return arr, status_st, filewrite
