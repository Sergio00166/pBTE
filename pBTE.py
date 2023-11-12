#Code by Sergio1260

from init import *

while True:
    #try:
        #Fix some things every time
        if len(arr)==0: arr.append("")
        if pointer==0: pointer=1
        if status_st==0: status=saved_df
        if pointer>columns+2:
            p_offset=len(text)-columns+2
            pointer=columns
            
          
        #A lot of stuff
        max_len=len(text); arr[line+offset-banoff]=text
        position="██"+black+str(line+offset-banoff)+reset+"█"*(4-len(str(line+offset-banoff)))
        all_file=fix_scr(arr[offset:rows+offset+1], arr, p_offset, black, reset, columns, line, offset, banoff)
        print(cls+position+"█"*4+status+banner+"█"*(72-len(filename))+black+filename+reset+"█\n", end="")
        print(all_file+"\n"*(rows-len(arr)+1)+bottom+("\r\033[%d;%dH"%(line+1, pointer)), end="")

        key=getch() #Read char
        
        if key==b'\xe0': #Directional arrows
            special_key=getch()
            if special_key==b'H': #Up
                pointer, oldptr, text, offset, line, p_offset =\
                up(line,offset,arr,text,banoff,oldptr,rows,pointer,p_offset)

            elif special_key==b'P': #Down
                pointer, oldptr, text, offset, line, p_offset =\
                down(line,offset,arr,text,banoff,oldptr,rows,pointer,p_offset)
     
            elif special_key==b'M': #Right
                if not pointer+p_offset>len(text)+1:
                    if not pointer>columns-1: pointer+=1
                    else: p_offset+=1
                oldptr=pointer
                
            elif special_key==b'K': #Left
                if not pointer==1: pointer-=1
                elif not p_offset==0: p_offset-=1
                oldptr=pointer
                
            elif special_key==b'S': #Supr
                text, arr =\
                supr(pointer, max_len, text, offset, banoff, arr, line, p_offset)

            elif special_key==b'G': pointer=1
            elif special_key==b'O': pointer=len(text)+1
            
        elif key==b'\x08': #Delete
            line, offset, text, arr, pointer, p_offset =\
            delete(pointer, text, offset, line, arr, banoff, p_offset)

        elif key==b'\r': #Return (adds new lines or moves text
            line, offset, arr, pointer, text =\
            newline(text, pointer, offset, banoff, line, arr, rows)       

        elif key==b'\x13': #Ctrl + S (SAVE)
            out=open(filename,"w",encoding="UTF-8")
            out.write("\n".join(arr)); out.close()
            status=saved_txt; status_st=2
            
        elif key==b'\x11': print("\033c",end=""); break #Ctrl + Q (EXIT)

        elif key==b'\x18': #Ctrl + X (CUT LINE)
            copy_buffer=arr[line+offset-banoff]
            arr.pop(line+offset-banoff)
            text=arr[line+offset-banoff]
            
        elif key==b'\x03': #Ctrl + C (COPY LINE)
            copy_buffer=arr[line+offset-banoff]
            
        elif key==b'\x10': #Ctrl + P (PASTE TEXT)
            if not len(copy_buffer)==0:
                p1=arr[:line+offset-banoff]; p2=arr[line+offset-banoff:]
                arr=p1+[copy_buffer]+p2; text=copy_buffer
        
        elif key==b'\x07': #Ctrl + G (go to line)
            line, offset = goto(rows, banoff, line, arr, offset, black, reset)

        elif key==b'\x01': #Ctrl + A (Save as)
            arr, status_st, filename =\
            save_as(filename, black, reset, rows, banoff, arr, saved_txt)
        
        else: #All the other keys
            p1=text[:pointer+p_offset-1]; p2=text[pointer+p_offset-1:]
            out=decode(key); text=(p1+out+p2);
            if p_offset==0: pointer+=1
            elif not p_offset+pointer>len(text)+2: p_offset+=1
            else: pointer+=1
        status_st-=1
        
    #except: pass
