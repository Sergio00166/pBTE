#Code by Sergio1260

from functions import decode, get_size
from upd_scr import menu_updsrc
from threading import Thread
from glob import glob
from os import getcwd, sep
from time import sleep as delay

def updscr_thr():
    global opentxt,openfile,rows,columns,black,reset,status,banoff,lenght
    global wrtptr,offset,line,arr,banner,filename,rows,columns,run,kill
    if not sep==chr(92): #If OS is LINUX
        #Get default values for TTY
        import sys; import termios; import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
    while not kill:
        delay(0.01)
        if run:
            mode=(openfile,opentxt,wrtptr,lenght)
            arg=(black,reset,status,banoff,offset,line,\
            wrtptr,arr,banner,filename,rows,columns)
            rows,columns = menu_updsrc(arg,mode)

def open_file(args):
    global opentxt,openfile,rows,columns,black,reset,status,banoff,lenght
    global wrtptr,offset,line,arr,banner,filename,rows,columns,run,kill

    filename,black,reset,rows,banoff,arr,columns,\
    status,offset,line,banner,status_st,getch,keys,pointer = args
    
    openfile=sep.join(filename.split(sep)[:-1])+sep
    opentxt=" Open: "; lenght=len(opentxt)+2; wrtptr=lenght+len(openfile)
    thr=Thread(target=updscr_thr); run=False; kill=False; thr.start()

    complete=False; cmp_counter=0
    
    while True:
        mode=(openfile,opentxt,wrtptr,lenght)
        arg=(black,reset,status,banoff,offset,line,\
        wrtptr,arr,banner,filename,rows,columns)
        rows,columns = menu_updsrc(arg,mode,True)

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
            wrtptr=len(openfile)+len(opentxt)+2
            complete=False
        
        elif key==keys["ctrl+o"]:
            try:
                openfile=glob(openfile, recursive=False)[0]
                tmp=open(openfile, "r", encoding="UTF-8").readlines(); arr=[]
                for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
                arr.append(""); filename=openfile
                run=False;kill=True;thr.join()
                print("\033c", end="")
                status_st=False
                pointer=offset=0
                line=1; break
            except: pass
            
        elif key==keys["ctrl+q"]:
            run=False;kill=True
            thr.join()
            print("\033c", end="")
            break
    
        elif key==keys["delete"]:
            if not wrtptr==lenght:
                if complete:
                    openfile=openfile.split(sep)[:-1]
                    openfile=sep.join(openfile)+sep
                    wrtptr-=len(openfile[-1])-1
                    complete=False
                else: 
                    p1=list(openfile)
                    p1.pop(wrtptr-lenght-1)
                    openfile="".join(p1)
                    wrtptr-=1

        elif key==keys["special"]:
            if not sep==chr(92): special_key=getch()
            arrow=getch()
            if arrow==keys["arr_left"]:
                if not wrtptr==lenght:
                    wrtptr-=1
            elif arrow==keys["arr_right"]:
                if not wrtptr>len(openfile)+lenght-1:
                    wrtptr+=1
            elif arrow==keys["supr"]:
                if not wrtptr==lenght:
                    if complete:
                        openfile=openfile.split(sep)[:-1]
                        openfile=sep.join(openfile)+sep
                        wrtptr-=len(openfile[-1])-1
                        complete=False
                    else: 
                        p1=list(openfile)
                        p1.pop(wrtptr-lenght)
                        openfile="".join(p1)
             
        elif key==keys["return"]: pass
        
        elif key==keys["ctrl+n"]:
            arr=[""]; filename=getcwd()+sep+"NewFile"
            print("\033c", end="")
            run=False;kill=True
            thr.join(); break
        
        else: #Rest of keys
            out=decode(key,getch)
            p1=openfile[:wrtptr-lenght]
            p2=openfile[wrtptr-lenght:]
            openfile=p1+out+p2
            wrtptr+=1
            complete=False

    return arr,filename,status_st,pointer,line,offset
