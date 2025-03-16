# Code by Sergio00166

from upd_scr import menu_updsrc
from time import sleep as delay
from scr_funcs import get_size
from threading import Thread
from functions import decode
from os import sep


if not sep==chr(92): #If OS is LINUX
    #Get default values for TTY
    from termios import TCSADRAIN,tcsetattr,tcgetattr
    from sys import stdin; from tty import setraw
    fd = stdin.fileno(); old_settings = tcgetattr(fd)

def updscr_thr():
    global prt_txt,entered_str,rows,columns,black,reset,status,banoff
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
            mode=(entered_str,prt_txt,wrtptr,lenght)
            arg=(black,bnc,slc,reset,status,banoff,offset,line,\
            wrtptr,arr,banner,filename,rows,columns,status_st)
            rows,columns = menu_updsrc(arg,mode)
            # If OS is LINUX set TTY to raw mode
            if not sep==chr(92): setraw(fd,when=TCSADRAIN)

def exit():
    global fd, old_settings, run, kill, thr
    run=False; kill=True; thr.join()
    if not sep == chr(92): tcsetattr(fd,TCSADRAIN,old_settings)


def chg_var_str(arg,kctlc_f=False):
    global prt_txt,entered_str,rows,columns,black,reset,status,banoff
    global lenght,wrtptr,offset,line,arr,banner,filename,rows,columns
    global run,kill,fd,old_settings,thr,status_st,bnc,slc

    filename,black,bnc,slc,reset,rows,banoff,arr,columns,status,offset,line,\
    banner,status_st,keys,cursor,select,read_key,entered_str,prt_txt = arg

    old_str = entered_str
    lenght=len(prt_txt)+2
    wrtptr=lenght+len(entered_str)
    thr=Thread(target=updscr_thr)
    run,kill,kctlc = False,False,False
    thr.daemon = True; thr.start()
    
    while True:
        # Fix when the cursor is out
        if len(entered_str)<wrtptr-lenght:
            wrtptr = len(entered_str)+lenght
        try:
            # If OS is LINUX restore TTY to it default values
            if not sep==chr(92):
                old=(fd,TCSADRAIN,old_settings)
                tcsetattr(fd, TCSADRAIN, old_settings)
            # Call Screen updater
            mode=(entered_str,prt_txt,wrtptr,lenght)
            arg=(black,bnc,slc,reset,status,banoff,offset,line,\
            wrtptr,arr,banner,filename,rows,columns,status_st)
            rows,columns = menu_updsrc(arg,mode,True)
            # If OS is LINUX set TTY to raw mode
            if not sep==chr(92): setraw(fd,when=TCSADRAIN)
            
            run=True #Start update screen thread
            key=read_key() #Map keys
            run=False #Stop update screen thread

            
            if key==keys["return"]: break

            elif key==keys["ctrl+c"]:
                entered_str = old_str
                if kctlc_f: kctlc=True
                break
        
            elif key==keys["delete"]:
                if not wrtptr==lenght:
                    p1=list(entered_str)
                    p1.pop(wrtptr-lenght-1)
                    entered_str="".join(p1)
                    wrtptr-=1

            elif key==keys["arr_left"]:
                if not wrtptr==lenght: wrtptr-=1
                
            elif key==keys["arr_right"]:
                if not wrtptr>len(entered_str)+lenght-1: wrtptr+=1
                    
            elif key==keys["supr"]:
                p1=list(entered_str)
                p1.pop(wrtptr-lenght)
                entered_str="".join(p1)

            elif key in keys["start"]: wrtptr=lenght
                
            elif key in keys["end"]: wrtptr=len(entered_str)+lenght
            
            else: #Rest of keys
                if wrtptr<((columns+2)*rows+1):
                    out=decode(key)
                    p1=entered_str[:wrtptr-lenght]
                    p2=entered_str[wrtptr-lenght:]
                    entered_str=p1+out+p2
                    wrtptr+=len(out)
                    complete=False
        except: pass

    exit() # Reset
    if kctlc: raise KeyboardInterrupt
    return entered_str

