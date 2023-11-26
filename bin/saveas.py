#Code by Sergio1260

from msvcrt import getch
from functions1 import decode, fix_out_tab,fix_read_tab

def save_as(filename,black,reset,rows,banoff,arr,saved_txt,status_st,columns,status,tabchr,tab_len):
    
    saveastxt="Save as: "; lenght=len(saveastxt)+2; filewrite=filename; wrtptr=lenght+len(filewrite)
    bottom="\n       "+black+"^Q"+reset+" CANCEL      "+black+"^S"+reset+" SAVE      "
    bottom+=black+"^B"+reset+" BACKUP      "+black+"^A"+reset+" APPEND      "
    bottom+=black+"^P"+reset+" PREPEND           "
    
    while True:
        out=saveastxt+filewrite; full=columns-len(out)
        print("\r\033[%d;%dH"%(rows+banoff+2, 1),end="")
        print("\r"+" "*(len(filewrite)+lenght+1), end="")
        print("\r"+black+out+(" "*full)+reset+bottom,end="")
        print("\r\033[%d;%dH"%(rows+banoff+2, wrtptr-1),end="")
        
        key=getch() #Map keys
        
        #Ctrl + S (confirms) or Ctrl + B backup
        if key==b'\x13' or key==b'\x02':
            try:
                
                if key==b'\x02' and filewrite==filename:
                    filewrite+=".bak" #Ctrl+B and if same name
                    
                out=open(filewrite,"w",encoding="UTF-8")
                arr=fix_out_tab(arr,tabchr,tab_len)
                out.write("\n".join(arr)); out.close(); status_st=True
                
                if key==b'\x13': #Ctr + S
                    status=saved_txt; tmp=open(filewrite, "r", encoding="UTF-8").readlines(); arr=[]
                    for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
                    arr.append(""); filename=filewrite
                    out=open(filewrite,"r",encoding="UTF-8")
                    arr=out.readlines()+[""]
                    arr=fix_read_tab(arr,tab_len,tabchr)
                    break
                    
                else: status=black+"Backed UP"+reset; break
                
            except: pass
            
        #Ctrl + Q (cancel)
        elif key==b'\x11': break
    
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
     
        elif key==b'\r': pass

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

    return arr, status_st, filename, status
