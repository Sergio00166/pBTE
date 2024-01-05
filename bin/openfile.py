#Code by Sergio1260

from msvcrt import getch
from functions import decode, update_scr, get_size
from threading import Thread
from glob import glob
from os import getcwd, sep
from time import sleep as delay

def updscr_thr():
    global saveastxt,openfile,rows,columns,black,reset,status,banoff,lenght
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
                update_scr(black,reset,status,banoff,offset,line,0,arr,banner,filename,rows,columns,True)
                print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
                print("\r"+" "*(len(openfile)+lenght), end="")
                print("\r"+black+out+(" "*full)+reset,end="")
                print("\r\033[%d;%dH"%(rows+banoff+2, wrtptr-1),end="")

def open_file(args):
    global saveastxt,openfile,rows,columns,black,reset,status,banoff,lenght
    global wrtptr,offset,line,arr,banner,filename,rows,columns,run,kill

    filename,black,reset,rows,banoff,arr,columns,status,offset,line,banner=args
    openfile=chr(92).join(filename.split(chr(92))[:-1])+chr(92)
    saveastxt=" Open: "; lenght=len(saveastxt)+2; wrtptr=lenght+len(openfile)
    thr=Thread(target=updscr_thr); run=False; kill=False; thr.start()

    complete=False; cmp_counter=0
    
    while True:
        out=saveastxt+openfile
        rows,columns=get_size()
        full=columns-len(out)+2
        update_scr(black,reset,status,banoff,\
        offset,line,0,arr,banner,filename,rows,columns)
        print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
        print("\r"+" "*(len(openfile)+lenght), end="")
        print("\r"+black+out+(" "*full)+reset,end="")
        print("\r\033[%d;%dH"%(rows+banoff+2, wrtptr-1),end="")

        run=True #Start update screen thread
        key=getch() #Map keys
        run=False #Stop update screen thread

        if key==b'\t':
            try:
                if openfile==sep or len(openfile)==0: raise ValueError
                if not complete: content=glob(openfile+"*",recursive=False)
                if len(content)>1: complete=True
                if complete:
                    openfile=content[cmp_counter]; cmp_counter+=1
                    if cmp_counter>=len(content): cmp_counter=0
                else: openfile=content[0]
            except: pass

        elif complete and key==b'\r':
            wrtptr=len(openfile)+len(saveastxt)+2
            complete=False
        
        #Ctrl + O (open)
        elif key==b'\x0f':
            try:
                openfile=glob(openfile, recursive=False)[0]
                tmp=open(openfile, "r", encoding="UTF-8").readlines(); arr=[]
                for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
                arr.append(""); filename=openfile
                run=False;kill=True;thr.join()
                print("\033c", end=""); break
            except: pass
            
        #Ctrl + Q (cancel)
        elif key==b'\x11':
            run=False;kill=True
            thr.join()
            print("\033c", end="")
            break
    
        elif key==b'\x08': #Delete
            if not wrtptr==lenght:
                if complete:
                    openfile=sep.join(openfile.split(sep)[:-1])+sep
                    wrtptr-=len(openfile.split(sep)[:-1])-2
                    complete=False
                else: 
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

        elif key==b'\r' or key==b'\n' or key==b'\t': pass
        
        #Ctrl + N
        elif key==b'\x0e':
            arr=[""]; filename=getcwd()+"\\NewFile"
            print("\033c", end="")
            run=False;kill=True
            thr.join(); break
        
        else: #Rest of keys
            if not wrtptr>columns-1:
                out=decode(key)
                p1=openfile[:wrtptr-lenght]
                p2=openfile[wrtptr-lenght:]
                openfile=p1+out+p2
                wrtptr+=1

    return arr, filename
