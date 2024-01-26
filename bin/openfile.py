#Code by Sergio1260

from functions import decode, update_scr, get_size
from threading import Thread
from glob import glob
from os import getcwd, sep
from time import sleep as delay

def updscr_thr():
    global saveastxt,openfile,rows,columns,black,reset,status,banoff,lenght
    global wrtptr,offset,line,arr,banner,filename,rows,columns,run,kill
    if not sep==chr(92): #If OS is LINUX
        #Get default values for TTY
        import sys; import termios; import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
    while not kill:
        delay(0.01)
        if run:
            old_rows=rows; old_columns=columns
            rows,columns=get_size()
            if rows<4: print("\r\033cTerminal too small")
            elif not (old_rows==rows and old_columns==columns):
                out=saveastxt+openfile
                rows,columns=get_size()
                full=columns-len(out)+2
                print("\r\033c",end="") #Clear screen
                # If OS is LINUX restore TTY to it default values
                if not sep==chr(92): termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                update_scr(black,reset,status,banoff,offset,line,0,arr,banner,filename,rows,columns)
                print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
                print("\r"+" "*(len(openfile)+lenght), end="")
                print("\r"+black+out+(" "*full)+reset,end="")
                print("\r\033[%d;%dH"%(rows+banoff+2, wrtptr-1),end="")
                # If OS is LINUX set TTY to raw mode
                if not sep==chr(92): tty.setraw(fd)

def open_file(args):
    global saveastxt,openfile,rows,columns,black,reset,status,banoff,lenght
    global wrtptr,offset,line,arr,banner,filename,rows,columns,run,kill

    filename,black,reset,rows,banoff,arr,columns,\
    status,offset,line,banner,status_st,getch,keys = args
    
    openfile=sep.join(filename.split(sep)[:-1])+sep
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

        if key==keys["tab"]:
            try:
                if not (openfile==sep or len(openfile)==0):
                    if not complete: content=glob(openfile+"*",recursive=False)
                    if len(content)>1: complete=True
                    if cmp_counter>=len(content): cmp_counter = 0
                    if complete:
                        openfile=content[cmp_counter]
                        cmp_counter+=1
                    else: openfile=content[0]
            except: pass

        elif complete and key==keys['return']:
            wrtptr=len(openfile)+len(saveastxt)+2
            complete=False
        
        elif key==keys["ctrl+o"]:
            try:
                openfile=glob(openfile, recursive=False)[0]
                tmp=open(openfile, "r", encoding="UTF-8").readlines(); arr=[]
                for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
                arr.append(""); filename=openfile
                run=False;kill=True;thr.join()
                print("\033c", end="")
                status_st=False; break
            except: pass
            
        elif key==keys["ctrl+q"]:
            run=False;kill=True
            thr.join()
            print("\033c", end="")
            break
    
        elif key==keys["delete"]:
            if not wrtptr==lenght:
                if complete:
                    openfile=sep.join(openfile.split(sep)[:-1])+sep
                    wrtptr-=len(openfile[-1])-1
                    complete=False
                else: 
                    p1=list(openfile); p1.pop(wrtptr-lenght-1)
                    openfile="".join(p1); wrtptr-=1

        elif key==keys["special"]:
            arrow=getch()
            if arrow==keys["arr_left"]:
                if not wrtptr==lenght:
                    wrtptr-=1
            elif arrow==keys["arr_right"]:
                if not wrtptr>len(openfile)+lenght-1:
                    wrtptr+=1

        elif key==keys["return"]: pass
        
        elif key==keys["ctrl+n"]:
            arr=[""]; filename=getcwd()+sep+"NewFile"
            print("\033c", end="")
            run=False;kill=True
            thr.join(); break
        
        else: #Rest of keys
            if not wrtptr>columns-1:
                out=decode(key,getch)
                p1=openfile[:wrtptr-lenght]
                p2=openfile[wrtptr-lenght:]
                openfile=p1+out+p2
                wrtptr+=1

    return arr, filename, status_st
