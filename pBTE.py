#Code by Sergio1260

def updscr_thr():
    global black,reset,legacy,status,banoff,offset,line,pointer,arr
    global banner,filename,rows,columns,run_thread,text,kill,p_offset
    while not kill:
        delay(0.01)
        if run_thread:
            old_rows=rows; old_columns=columns
            rows,columns=get_size()
            if not (old_rows==rows and old_columns==columns):
                if len(arr)==0: arr.append("")
                if pointer==0: pointer=1
                if status_st==0: status=saved_df
                max_len=len(text)
                arr[line+offset-banoff]=text
                if line>rows:
                    offset=offset+(line-rows)
                    line=rows
            
                update_scr(black,reset,legacy,status,banoff,offset,\
                line,pointer,arr,banner,filename,rows,columns)

from sys import path
path.append(path[0]+"\\bin")
from init import *
update_thr=Thread(target=updscr_thr)
run_thread=True; kill=False
update_thr.start()

while True:
    try:
        if len(arr)==0: arr.append("")
        if pointer==0: pointer=1
        if status_st==0: status=saved_df
        max_len=len(text)
        arr[line+offset-banoff]=text
        rows,columns=get_size()
        update_scr(black,reset,legacy,status,banoff,offset,\
        line,pointer,arr,banner,filename,rows,columns)
        
        run_thread=True #Start update Thread
        key=getch() #Read char
        run_thread=False #Stop update Thread
       
        if key==b'\x11': #Ctrl + Q (EXIT)
            kill=True; update_thr.join()
            print("\033c",end=""); break
            
        else:
            #Call keys functions (Yeah, its a lot of args and returned values)
            text,pointer,oldptr,line,offset,columns,banoff,arr,rows,\
            max_len,filename,status,status_st,copy_buffer,fixstr,fix,\
            ch_T_SP,= keys(key,text,pointer,oldptr,line,offset,columns,\
            banoff,arr,rows,max_len,filename,status,status_st,copy_buffer,\
            fixstr,fix,black,reset,saved_txt,ch_T_SP,legacy,banner)
        
    except: pass
