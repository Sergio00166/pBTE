#Code by Sergio1260

from functions1 import decode, get_size, read_UTF8
from upd_scr import menu_updsrc
from threading import Thread
from glob import glob
from os import getcwd, sep
from time import sleep as delay

if not sep==chr(92): #If OS is LINUX
    #Get default values for TTY
    from termios import TCSADRAIN,\
    tcsetattr, tcgetattr, ICANON, ECHO
    from sys import stdin
    fd = stdin.fileno()
    old_settings = tcgetattr(fd)

def updscr_thr():
    global opentxt,openfile,rows,columns,black,reset,status,banoff
    global lenght,wrtptr,offset,line,arr,banner,filename,rows,columns
    global run, kill, fd, old_settings, status_st, bnc, slc
    
    while not kill:
        delay(0.01)
        if run:
            # If OS is LINUX restore TTY to it default values
            if not sep==chr(92):
                old=(fd,TCSADRAIN,old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            mode=(openfile,opentxt,wrtptr,lenght)
            arg=(black,bnc,slc,reset,status,banoff,offset,line,\
            wrtptr,arr,banner,filename,rows,columns,status_st)
            rows,columns = menu_updsrc(arg,mode)
            # If OS is LINUX set TTY to raw mode
            if not sep==chr(92):
                terminal = tcgetattr(fd)
                terminal[3] = terminal[3] & ~(ICANON | ECHO)
                tcsetattr(fd, TCSADRAIN, terminal)

def exit():
    global fd, old_settings, run, kill, thr
    run=False; kill=True; thr.join()
    if not sep == chr(92): tcsetattr(fd,TCSADRAIN,old_settings)
    print(reset+"\r\033c", end="")


def open_file(arg):
    global opentxt,openfile,rows,columns,black,reset,status,banoff
    global lenght,wrtptr,offset,line,arr,banner,filename,rows,columns
    global run, kill, fd, old_settings, thr, status_st, bnc, slc

    filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,offset,\
    line,banner,status_st,keys,pointer,fixstr,select,read_key = arg
    
    openfile=sep.join(filename.split(sep)[:-1])+sep
    opentxt=" Open: "; lenght=len(opentxt)+2; wrtptr=lenght+len(openfile)
    thr=Thread(target=updscr_thr); run=False; kill=False; thr.start()
    complete=False; cmp_counter=0
    
    while True:
        # Fix when the pointer is out
        if len(openfile)<wrtptr-lenght:
            wrtptr = len(openfile)+lenght
        try:
            # If OS is LINUX restore TTY to it default values
            if not sep==chr(92):
                old=(fd,TCSADRAIN,old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            mode=(openfile,opentxt,wrtptr,lenght)
            arg=(black,bnc,slc,reset,status,banoff,offset,line,\
            wrtptr,arr,banner,filename,rows,columns,status_st)
            rows,columns = menu_updsrc(arg,mode,True)
            # If OS is LINUX set TTY to raw mode
            if not sep==chr(92):
                terminal = tcgetattr(fd)
                terminal[3] = terminal[3] & ~(ICANON | ECHO)
                tcsetattr(fd, TCSADRAIN, terminal)

            run=True #Start update screen thread
            key=read_key() #Map keys
            run=False #Stop update screen thread

            if key==keys["tab"]:
                if not (openfile==sep or len(openfile)==0):
                    if not complete: content=glob(openfile+"*",recursive=False)
                    if len(content)>0: complete=True
                    if cmp_counter>=len(content): cmp_counter = 0
                    if complete:
                        openfile=content[cmp_counter]
                        cmp_counter+=1
                    else: openfile=content[0]

            elif complete and key==keys['return']:
                wrtptr=len(openfile)+len(opentxt)+2
                complete=False

            elif key==keys["return"]: pass
            
            elif key==keys["ctrl+o"]:
                openfile=glob(openfile, recursive=False)[0]
                arr=read_UTF8(openfile); filename=openfile
                status_st,line,select = False,1,[]
                pointer=offset=0; exit(); break
                
            elif key==keys["exit"]: exit(); break
        
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

            elif key==keys["arr_left"]:
                if not wrtptr==lenght: wrtptr-=1
                
            elif key==keys["arr_right"]:
                if not wrtptr>len(openfile)+lenght-1: wrtptr+=1
                    
            elif key==keys["supr"]:
                if not sep==chr(92): getch()
                if complete:
                    openfile=openfile.split(sep)[:-1]
                    openfile=sep.join(openfile)+sep
                    wrtptr-=len(openfile[-1])-1
                    complete=False
                else:
                    p1=list(openfile)
                    p1.pop(wrtptr-lenght)
                    openfile="".join(p1)

            elif key==keys["start"]: wrtptr=lenght
                
            elif key==keys["end"]: wrtptr=len(openfile)+lenght
            
            elif key==keys["ctrl+n"]:
                pointer,offset,line = 1,0,1
                arr,select = [""],[]
                filename=getcwd()+sep+"NewFile"
                exit(); break
            
            else: #Rest of keys
                cond1=wrtptr<((columns+2)*rows+1)
                cond2=str(key)[4:6] in fixstr
                if cond1 and not cond2:
                    out=decode(key)
                    p1=openfile[:wrtptr-lenght]
                    p2=openfile[wrtptr-lenght:]
                    openfile=p1+out+p2
                    wrtptr+=1
                    complete=False
        except: pass
    
    return arr,filename,status_st,pointer,line,offset,select
