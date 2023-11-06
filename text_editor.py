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
banner="█"*40+black+"BASIC TEXT EDITOR"+reset+"█"*46+"\n\n"
bottom="\n\n "+black+"^Q"+reset+" EXIT   "+black+"^S"+reset+" SAVE   "
bottom+=black+"^X"+reset+" CUT   "+black+"^C"+reset+" COPY   "
bottom+=black+"^P"+reset+" PASTE   "+black+"^G"+reset+" GOTO"
copy_buffer=""; cls="\033c"

saved_txt=black+"SAVED"+reset; status=saved_df="█"*5; status_st=0

while True:
    try:
        if len(arr)==0: arr.append("")
        if pointer==0: pointer=1
        if line==1: line=2
        if status_st==0: status=saved_df
        
        max_len=len(text); arr[line+offset-banoff]=text
        position="██"+black+str(line+offset-banoff)+reset+"█"*(4-len(str(line+offset-banoff)))
        all_file="\n".join(arr[offset:rows+offset+1])+"\n"*(rows-len(arr))
        print(cls+position+banner+all_file+bottom+("\r\033[%d;%dH"%(line+1, pointer)),end="")
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

        elif key==b'\x13': #Ctrl + S (SAVE)
            out=open(filename,"w",encoding="UTF-8")
            out.write("\n".join(arr)); out.close()
            status=saved_txt; status_st=2
            
        elif key==b'\x11': print("\033c",end=""); break #Ctrl + Q (EXIT)

        elif key==b'\x18': #Ctrl + X (CUT LINE)
            copy_buffer=arr[line+offset-banoff]
            arr.pop(line+offset-banoff)
            text=arr[line+offset-banoff]
            
        elif key==b'\x03': #Ctrl + C (COPY LINE)
            copy_buffer=arr[line+offset-banoff]
            
        elif key==b'\x10': #Ctrl + P (PASTE TEXT)
            if not len(copy_buffer)==0:
                p1=arr[:line+offset-banoff]
                p2=arr[line+offset-banoff:]
                arr=p1+[copy_buffer]+p2
                text=copy_buffer
    
        elif key==b'\x07': #Ctrl + G (go to line)
            print(" "*len(text)+"\r\033[%d;%dH"%(line+1, 1),end="")
            print(black+" Go to line:"+reset, end=" ")
            p1=input()
            try:
                p1=int(p1)+1
                if not p1<1 and p1<len(arr):
                    if p1<rows-banoff-1: line=p1; offset=1
                    else: line=(p1-banoff)//rows-1; offset=p1-line+1
            except:
                print("\r\033[%d;%dH"%(line+1, 1),end="")
                print(text)
            
        else: #All the other keys
            p1=text[:pointer-1]; p2=text[pointer-1:]
            text=(p1+key.decode('utf-8')+p2)
            pointer+=1
        status_st-=1

    except Exception as e: print("\033c"+str(e)); input(); break
