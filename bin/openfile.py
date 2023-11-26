#Code by Sergio1260

from msvcrt import getch
from fixes import decode,fix_read_tab

def open_file(filename,black,reset,rows,banoff,arr,columns,tab_len,tabchr):
    
    saveastxt="Open: "; lenght=len(saveastxt)+2; openfile=filename; wrtptr=lenght+len(openfile)
    bottom="\n            "+black+"^Q"+reset+" CANCEL                "
    bottom+=black+"^O"+reset+" OPEN                "
    bottom+=black+"^N"+reset+" NEW FILE                "
    
    while True:
        out=saveastxt+openfile; full=columns-len(out)
        print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
        print("\r"+" "*(len(openfile)+lenght+1), end="")
        print("\r"+black+out+(" "*full)+reset+bottom,end="")
        print("\r\033[%d;%dH"%(rows+banoff+2, wrtptr-1),end="")
        
        key=getch() #Map keys
        
        #Ctrl + O (open)
        if key==b'\x0f':
            try:
                tmp=open(openfile, "r", encoding="UTF-8").readlines(); arr=[]
                for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
                arr=fix_read_tab(arr,tab_len,tabchr)
                arr.append(""); filename=openfile; break
            except: pass
            
        #Ctrl + Q (cancel)
        elif key==b'\x11': break
    
        elif key==b'\x08': #Delete
            if not wrtptr==lenght:
                p1=list(openfile); p1.pop(wrtptr-lenght-1)
                openfile="".join(p1); wrtptr-=1

        elif key==b'\xe0': #Arrows
            arrow=getch()
            if arrow==b'K': #Left
                if not wrtptr==lenght:
                    wrtptr-=1
            elif arrow==b'M': #Right
                if not wrtptr>len(openfile)+lenght-1:
                    wrtptr+=1

        #Block intro
        elif key==b'\r': pass
        
        #Ctrl + N
        elif key==b'\x0e':
            arr=[""]; filename=getcwd()+"\\NewFile"
            break
        
        else: #Rest of keys
            if not wrtptr>columns-1:
                out=decode(key)
                p1=openfile[:wrtptr-lenght]
                p2=openfile[wrtptr-lenght:]
                openfile=p1+out+p2
                wrtptr+=1

    return arr, filename
