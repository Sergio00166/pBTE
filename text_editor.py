#Code by Sergio1260

from msvcrt import getch
from os import get_terminal_size, getcwd
from sys import argv
from os.path import exists

def fixlenline(text, pointer):
    length=len(text)
    if pointer>length: return length
    else: return pointer

if not len(argv)==1: filename=" ".join(argv[1:])
else: filename=str(input("File to open: "))
if not ":\\" in filename: filename=getcwd()+"\\"+filename

if exists(filename):
    tmp=open(filename, "r", encoding="UTF-8").readlines(); arr=[]
    for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
    arr.append("")
else: arr=[""]

text=arr[0]; pointer=offset=0; line=banoff=2
black="[47m[30m[2m"; reset="[0m"; rows=get_terminal_size()[0]//5
banner="\033c"+"█"*46+black+"BASIC TEXT EDITOR"+reset+"█"*46+"\n\n"
bottom="\n\n "+black+"^O"+reset+" Write out   "+black+"^X"+reset+" EXIT  "

saved_txt=black+"SAVED"+reset; status=saved_df="█"*5; status_st=0

while True:
    try:
        if len(arr)==0: arr.append("")
        if pointer==0: pointer=1
        if line==1: line=2
        if status_st==0: status=saved_df
        
        extra=black+"File: "+filename+"  "+reset
        extra_len=(96-len(extra))//2
        extra="█"*extra_len+status+"█"*(extra_len+1)+extra
        arr[line+offset-banoff]=text; max_len=len(text)
        all_file="\n".join(arr[offset:rows+offset+1])+"\n"*(rows-len(arr)+1)
        print(banner+all_file+bottom+extra+("\r\033[%d;%dH"%(line+1, pointer)),end="")
        key=getch()
        
        if key==b'\xe0': #Directional arrows
            arrow_key=getch()
            if arrow_key==b'H': #Up
                if not line==banoff:
                    line-=1; text=arr[line+offset-banoff]
                    pointer=fixlenline(text, pointer)
                elif offset>0: offset-=1; line+=1

            elif arrow_key==b'P': #Down
                if not line+offset==len(arr)+banoff-1:
                    if not line==rows+banoff:
                        line+=1; text=arr[line+offset-banoff]
                        pointer=fixlenline(text, pointer)
                    elif not line+offset==len(arr)+1:
                        offset+=1; line-=1
                    
            elif arrow_key==b'M': #Right
                if not pointer>max_len:
                    pointer+=1
                    
            elif arrow_key==b'K': #Left
                if not pointer==1:
                    pointer-=1
                    
            elif arrow_key==b'S': #Supr
                if not pointer==max_len+1:
                    p1=list(text); p1.pop(pointer-1)
                    text="".join(p1)
                elif not line+offset==1: #move all to previous line
                    seltext=arr[line+offset-banoff+1]
                    arr[line+offset-banoff+1]=text+seltext
                    arr.pop(line+offset-banoff+1)
                    text=text+seltext
                
        elif key==b'\x08': #Delete
            if not pointer==1: #Delete char
                p1=list(text); p1.pop(pointer-2)
                text="".join(p1); pointer-=1
            elif not line+offset==1: #move all to previous line
                seltext=arr[line+offset-banoff-1]
                arr[line+offset-banoff-1]=seltext+text
                arr.pop(line+offset-banoff)
                pointer=len(seltext)+1
                text=seltext+text
                if not offset==0:
                    offset-=1
                else: line-=1
                      
        elif key==b'\r': #Return
            seltext=[text[:pointer-1]]
            if not line+offset==len(arr):
                p1=arr[:line+offset-banoff]
                p2=arr[line+offset-banoff:]
                if not len(text)==0:
                    seltext=[text[:pointer-1]]
                    arr=p1+seltext+p2
                    text=text[pointer-1:]
                    pointer=0    
                else: arr=p1+[""]+p2
            else:
                if not len(text)==0:
                    arr.append(seltext)
                    text=text[pointer-1:]
                    pointer=0    
                else: arr.append("")
            if not line>rows+1: line+=1
            else: offset+=1

        elif key==b'\x0f': #Ctrl + O (SAVE)
            out=open(filename,"w",encoding="UTF-8")
            out.write("\n".join(arr)); out.close()
            status=saved_txt; status_st=2
            
        elif key==b'\x18': print("\033c",end=""); break #Ctrl + X (EXIT)
        
        else: #All the other keys
            p1=text[:pointer-1]; p2=text[pointer-1:]
            text=(p1+key.decode('utf-8')+p2)
            pointer+=1
        status_st-=1
    except: pass

