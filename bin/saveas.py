#Code by Sergio1260

from msvcrt import getch
from functions import decode
from screenmgr import update_scr
from functions import get_size
from threading import Thread
from time import sleep as delay

def updscr_thr():
    global saveastxt,filewrite,rows,columns,black,reset,legacy,status,banoff
    global lenght,wrtptr,offset,line,arr,banner,filename,rows,columns,run,kill
    while not kill:
        delay(0.01)
        if run:
            old_rows=rows; old_columns=columns
            rows,columns=get_size()
            if not (old_rows==rows and old_columns==columns):
                out=saveastxt+filewrite
                rows,columns=get_size()
                full=columns-len(out)+2
                update_scr(black,reset,legacy,status,banoff,offset,line,0,arr,banner,filename,rows,columns)
                print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
                print("\r"+" "*(len(filewrite)+lenght), end="")
                print("\r"+black+out+(" "*full)+reset,end="")
                print("\r\033[%d;%dH"%(rows+banoff+2, wrtptr-1),end="")

def save_as(args):
    global saveastxt,filewrite,rows,columns,black,reset,legacy,status,banoff
    global lenght,wrtptr,offset,line,arr,banner,filename,rows,columns,run,kill

    filename,black,reset,rows,banoff,arr,columns,legacy,status,offset,line,banner,status_st,saved_txt=args
    saveastxt=" Save as: "; lenght=len(saveastxt)+2; filewrite=filename; wrtptr=lenght+len(filewrite)
    thr=Thread(target=updscr_thr); run=False; kill=False; thr.start() 
    
    while True:
        out=saveastxt+filewrite
        rows,columns=get_size()
        full=columns-len(out)+2
        update_scr(black,reset,legacy,status,banoff,\
        offset,line,0,arr,banner,filename,rows,columns)
        print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
        print("\r"+" "*(len(filewrite)+lenght), end="")
        print("\r"+black+out+(" "*full)+reset,end="")
        print("\r\033[%d;%dH"%(rows+banoff+2, wrtptr-1),end="")
        
        run=True #Start update screen thread
        key=getch() #Map keys
        run=False #Stop update screen thread
        
        #Ctrl + A (confirms) or Ctrl + B backup
        if key==b'\x01' or key==b'\x02':
            try:
                if key==b'\x02' and filewrite==filename:
                    filewrite+=".bak" #Ctrl+B and if same name    
                out=open(filewrite,"w",encoding="UTF-8")
                out.write("\n".join(arr)); out.close(); status_st=True
                if key==b'\x01': #Ctr + A
                    status=saved_txt; tmp=open(filewrite, "r", encoding="UTF-8").readlines(); arr=[]
                    for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
                    arr.append(""); filename=filewrite
                    out=open(filewrite,"r",encoding="UTF-8")
                    run=False;kill=True
                    thr.join(); break
                else:
                    status=black+"BkUPd"+reset
                    run=False;kill=True
                    thr.join(); break
            except: pass
            
        #Ctrl + Q (cancel)
        elif key==b'\x11':
            run=False;kill=True
            thr.join(); break
    
        elif key==b'\x08': #Delete
            if not wrtptr==lenght:
                p1=list(filewrite); p1.pop(wrtptr-lenght-1)
                filewrite="".join(p1); wrtptr-=1

        elif key==b'\xe0': #Arrows
            arrow=getch()
            if arrow==b'K': #Left
                if not wrtptr==lenght:
                    wrtptr-=1
            elif arrow==b'M': #Right
                if not wrtptr>len(filewrite)+lenght-1:
                    wrtptr+=1
     
        elif key==b'\r' or key==b'\n': pass

        elif key==b'\x10' or key==b'\x01': #Ctrl + P or Ctrl + A
            try:
                tmp=open(filewrite, "r", encoding="UTF-8").readlines()
                status=saved_txt
                if key==b'\x01': output=list(arr+tmp)
                elif key==b'\x10': output=list(tmp+arr)
                out=open(filewrite, "w", encoding="UTF-8")
                out.write("\n".join(output)); break
            except: pass
        
        else: #Rest of keys
            if not wrtptr>columns-1:
                out=decode(key)
                p1=filewrite[:wrtptr-lenght]
                p2=filewrite[wrtptr-lenght:]
                filewrite=p1+out+p2
                wrtptr+=1

    return status_st, filename, status
