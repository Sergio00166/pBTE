#Code by Sergio1260

from functions import decode, get_size
from upd_scr import menu_updsrc
from threading import Thread
from os import sep
from time import sleep as delay
from glob import glob

def updscr_thr():
    global saveastxt,filewrite,rows,columns,black,reset,status,banoff
    global lenght,wrtptr,offset,line,arr,banner,filename,rows,columns,run,kill
    
    if not sep==chr(92): #If OS is LINUX
        #Get default values for TTY
        import sys; import termios; import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
    while not kill:
        delay(0.01)
        if run:
            mode=(filewrite,saveastxt,wrtptr,lenght)
            arg=(black,reset,status,banoff,offset,line,\
            wrtptr,arr,banner,filename,rows,columns)
            rows,columns = menu_updsrc(arg,mode)

def save_as(args):
    global saveastxt,filewrite,rows,columns,black,reset,status,banoff
    global lenght,wrtptr,offset,line,arr,banner,filename,rows,columns,run,kill

    filename,black,reset,rows,banoff,arr,columns,status,\
    offset,line,banner,status_st,saved_txt,getch,keys = args
    saveastxt=" Save as: "; lenght=len(saveastxt)+2
    filewrite=filename; wrtptr=lenght+len(filewrite)
    thr=Thread(target=updscr_thr); run=False
    kill=False; thr.start(); complete=False; cmp_counter=0
    
    while True:
        mode=(filewrite,saveastxt,wrtptr,lenght)
        arg=(black,reset,status,banoff,offset,line,\
        wrtptr,arr,banner,filename,rows,columns)
        rows,columns = menu_updsrc(arg,mode,True)
        
        run=True #Start update screen thread
        key=getch() #Map keys
        run=False #Stop update screen thread

        if key==keys["tab"]:
            try:
                if not (filewrite==sep or len(filewrite)==0):
                    if not complete: content=glob(filewrite+"*",recursive=False)
                    if len(content)>1: complete=True
                    if cmp_counter>=len(content): cmp_counter = 0
                    if complete:
                        filewrite=content[cmp_counter]
                        cmp_counter+=1
                    else: filewrite=content[0]
            except: pass

        elif complete and key==keys["return"]:
            wrtptr=len(filewrite)+len(saveastxt)+2
            complete=False
        
        #Ctrl + A (confirms) or Ctrl + B backup
        elif key==keys["ctrl+a"] or key==keys["ctrl+b"]:
            try:
                if key==["ctrl+b"] and filewrite==filename:
                    filewrite+=".bak"
                out=open(filewrite,"w",encoding="UTF-8")
                out.write("\n".join(arr)); out.close(); status_st=True
                if key==keys["ctrl+a"]:
                    status=saved_txt; tmp=open(filewrite, "r", encoding="UTF-8").readlines(); arr=[]
                    for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
                    arr.append(""); filename=filewrite
                    out=open(filewrite,"r",encoding="UTF-8")
                    run=False;kill=True; thr.join()
                    print("\033c", end=""); break
                else:
                    status=black+"BkUPd"+reset
                    run=False;kill=True; thr.join()
                    print("\033c", end=""); break
            except: pass
            
        elif key==keys["ctrl+q"]:
            run=False;kill=True; thr.join()
            print("\033c", end=""); break
    
        elif key==keys["delete"]:
            if not wrtptr==lenght:
                if complete:
                    filewrite=filewrite.split(sep)[:-1]
                    filewrite=sep.join(filewrite)+sep
                    wrtptr-=len(filewrite[-1])-1
                    complete=False
                else: 
                    p1=list(filewrite)
                    p1.pop(wrtptr-lenght-1)
                    filewrite="".join(p1)
                    wrtptr-=1

        elif key==keys["special"]:
            if not sep==chr(92): special_key=getch()
            arrow=getch()
            if arrow==keys["arr_left"]:
                if not wrtptr==lenght:
                    wrtptr-=1
            elif arrow==keys["arr_right"]:
                if not wrtptr>len(filewrite)+lenght-1:
                    wrtptr+=1
            elif arrow==keys["supr"]:
                if not wrtptr==lenght:
                    if complete:
                        filewrite=sep.join(filewrite.split(sep)[:-1])+sep
                        wrtptr-=len(filewrite[-1])-1
                        complete=False
                    else: 
                        p1=list(filewrite)
                        p1.pop(wrtptr-lenght)
                        filewrite="".join(p1)       
     
        elif key==keys["return"]: pass

        elif key==keys["ctrl+p"] or key==keys["ctrl+a"]:
            try:
                tmp=open(filewrite, "r", encoding="UTF-8").readlines()
                status=saved_txt
                if key==keys["ctrl+a"]: output=list(arr+tmp)
                elif key==keys["ctrl+p"]: output=list(tmp+arr)
                out=open(filewrite, "w", encoding="UTF-8")
                out.write("\n".join(output)); break
            except: pass
        
        else: #Rest of keys
            out=decode(key,getch)
            p1=filewrite[:wrtptr-lenght]
            p2=filewrite[wrtptr-lenght:]
            filewrite=p1+out+p2
            wrtptr+=1

    return status_st, filename, status
