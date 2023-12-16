#Code by Sergio1260

from msvcrt import getch
from functions import decode
from glob import glob
from os import getcwd
from screenmgr import update_scr
from functions import get_size
from threading import Thread
from time import sleep as delay

def updscr_thr():
    global saveastxt,openfile,rows,columns,black,reset,legacy,status,banoff,lenght
    global wrtptr,offset,line,arr,banner,filename,rows,columns,run,kill
    while not kill:
        delay(0.01)
        if run:
            old_rows=rows; old_columns=columns
            rows,columns=get_size()
            if not (old_rows==rows and old_columns==columns):
                out=saveastxt+openfile
                rows,columns=get_size()
                full=columns-len(out)+2
                update_scr(black,reset,legacy,status,banoff,offset,line,0,arr,banner,filename,rows,columns)
                print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
                print("\r"+" "*(len(openfile)+lenght), end="")
                print("\r"+black+out+(" "*full)+reset,end="")
                print("\r\033[%d;%dH"%(rows+banoff+2, wrtptr-1),end="")

def open_file(args):
    global saveastxt,openfile,rows,columns,black,reset,legacy,status,banoff,lenght
    global wrtptr,offset,line,arr,banner,filename,rows,columns,run,kill

    filename,black,reset,rows,banoff,arr,columns,legacy,status,offset,line,banner=args
    openfile=chr(92).join(filename.split(chr(92))[:-1])+chr(92)
    saveastxt=" Open: "; lenght=len(saveastxt)+2; wrtptr=lenght+len(openfile)
    thr=Thread(target=updscr_thr); run=False; kill=False; thr.start() 
    
    while True:
        out=saveastxt+openfile
        rows,columns=get_size()
        full=columns-len(out)+2
        update_scr(black,reset,legacy,status,banoff,\
        offset,line,0,arr,banner,filename,rows,columns)
        print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
        print("\r"+" "*(len(openfile)+lenght), end="")
        print("\r"+black+out+(" "*full)+reset,end="")
        print("\r\033[%d;%dH"%(rows+banoff+2, wrtptr-1),end="")

        run=True #Start update screen thread
        key=getch() #Map keys
        run=False #Stop update screen thread
        
        #Ctrl + O (open)
        if key==b'\x0f':
            try:
                openfile=glob(openfile, recursive=False)[0]
                tmp=open(openfile, "r", encoding="UTF-8").readlines(); arr=[]
                for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
                arr.append(""); filename=openfile
                break
            except: pass
            
        #Ctrl + Q (cancel)
        elif key==b'\x11':
            run=False;kill=True
            thr.join(); break
    
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
        elif key==b'\r' or key==b'\n': pass
        
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
