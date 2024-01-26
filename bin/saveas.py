#Code by Sergio1260

from functions import decode, update_scr, get_size
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
            old_rows=rows; old_columns=columns
            rows,columns=get_size()
            if rows<4: print("\r\033cTerminal too small")
            elif not (old_rows==rows and old_columns==columns):
                out=saveastxt+filewrite
                rows,columns=get_size()
                full=columns-len(out)+2
                print("\r\033c",end="") #Clear screen
                # If OS is LINUX restore TTY to it default values
                if not sep==chr(92): termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                update_scr(black,reset,status,banoff,offset,line,0,arr,banner,filename,rows,columns)
                print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
                print("\r"+" "*(len(filewrite)+lenght), end="")
                print("\r"+black+out+(" "*full)+reset,end="")
                print("\r\033[%d;%dH"%(rows+banoff+2, wrtptr-1),end="")
                # If OS is LINUX set TTY to raw mode
                if not sep==chr(92): tty.setraw(fd)

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
        out=saveastxt+filewrite
        rows,columns=get_size()
        full=columns-len(out)+2
        update_scr(black,reset,status,banoff,\
        offset,line,0,arr,banner,filename,rows,columns)
        print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
        print("\r"+" "*(len(filewrite)+lenght), end="")
        print("\r"+black+out+(" "*full)+reset,end="")
        print("\r\033[%d;%dH"%(rows+banoff+2, wrtptr-1),end="")
        
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
                    filewrite=sep.join(filewrite.split(sep)[:-1])+sep
                    wrtptr-=len(filewrite[-1])-1
                    complete=False
                else: 
                    p1=list(filewrite); p1.pop(wrtptr-lenght-1)
                    filewrite="".join(p1); wrtptr-=1

        elif key==keys["special"]:
            arrow=getch()
            if arrow==keys["arr_left"]:
                if not wrtptr==lenght:
                    wrtptr-=1
            elif arrow==keys["arr_right"]:
                if not wrtptr>len(filewrite)+lenght-1:
                    wrtptr+=1
     
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
            if not wrtptr>columns-1:
                out=decode(key,getch)
                p1=filewrite[:wrtptr-lenght]
                p2=filewrite[wrtptr-lenght:]
                filewrite=p1+out+p2
                wrtptr+=1

    return status_st, filename, status
