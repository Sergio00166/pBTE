#Code by Sergio1260

from functions import *
from actions import *
from saveas import save_as
from openfile import open_file

def keys_func(key,text,pointer,oldptr,line,offset,columns,banoff,arr,rows,\
              max_len,filename,status,status_st,copy_buffer,fixstr,fix,\
              black,reset,saved_txt,ch_T_SP,banner,getch,keys):
        
    if key==keys["special"]:
        if not sep==chr(92): special_key=getch()
        special_key=getch() #Read char
        
        if special_key==keys["arr_up"]:
            pointer, oldptr, text, offset, line =\
            up(line,offset,arr,text,banoff,oldptr,rows,pointer)
            
        elif special_key==keys["arr_down"]:
            pointer, oldptr, text, offset, line =\
            down(line,offset,arr,text,banoff,oldptr,rows,pointer)
            
        elif special_key==keys["arr_right"]:
            text, pointer, oldptr, line, offset =\
            right(pointer,text,columns,offset,line,banoff,arr,rows,oldptr)
            
        elif special_key==keys["arr_left"]:
            pointer, oldptr, text, line, offset =\
            left(pointer,oldptr,line,offset,banoff,text,arr)
            
        elif special_key==keys["supr"]:
            text,arr = supr(pointer,max_len,text,offset,banoff,arr,line)
            if not sep==chr(92): getch()
            status_st=False
            
        elif special_key==keys["start"]:
            pointer=1; p_offset=0; oldptr=pointer
            
        elif special_key==keys["end"]:
            pointer=len(text)+1; oldptr=pointer
            
        elif special_key==keys["repag"]:
            p1=line+offset-banoff-rows
            if p1<0: p1=0
            line, offset, text =\
            CalcRelLine(p1,arr,offset,line,banoff,rows)
            if not sep==chr(92): getch()
            
        elif special_key==keys["avpag"]:
            p1=line+offset-banoff+rows
            if p1>=len(arr): p1="-"
            line, offset, text =\
            CalcRelLine(p1,arr,offset,line,banoff,rows)
            if not sep==chr(92): getch()

        
    elif key==keys["delete"]:
         line,offset, text, arr, pointer =\
         backspace(pointer,text,offset,line,arr,banoff)
         status_st=False

    elif key==keys["return"]:
        line,offset,arr,pointer,text =\
        newline(text,pointer,offset,banoff,line,arr,rows)
        status_st=False

    elif key==keys["ctrl+s"]:
        out=open(filename,"w",encoding="UTF-8")
        out.write("\n".join(arr)); out.close()
        status=saved_txt; status_st=True
        out=open(filename,"r",encoding="UTF-8")
        
    elif key==keys["ctrl+x"]:
        if line+offset>len(arr)-1:
            copy_buffer=text[pointer-1:]; text=text[:pointer-1]
        else:
            copy_buffer=arr[line+offset-banoff]
            arr.pop(line+offset-banoff)
            text=arr[line+offset-banoff]
        status_st=False
        
    elif key==keys["ctrl+c"]:
        copy_buffer=arr[line+offset-banoff][pointer-1:]
        
    elif key==keys["ctrl+p"]:
        if not len(copy_buffer)==0:
            p1=arr[:line+offset-banoff]; p2=arr[line+offset-banoff+1:]
            fix1=text[:pointer-1]; fix2=text[+pointer-1:]
            out=fix1+copy_buffer+fix2; arr=p1+[out]+p2; text=out
            pointer=len(fix1+copy_buffer); status_st=False

    elif key==keys["ctrl+g"]:
        line, offset ,text =\
        goto(rows,banoff,line,arr,offset,black,reset)

    elif key==keys["ctrl+a"]:
        args = (filename,black,reset,rows,banoff,arr,columns,\
        status,offset,line,banner,status_st,saved_txt,getch,keys,fixstr)
        status_st, filename, status = save_as(args)

    elif key==keys["ctrl+o"]:
        args = (filename,black,reset,rows,banoff,arr,columns,\
        status,offset,line,banner,status_st,getch,keys,pointer,fixstr)
        arr,filename,status_st,pointer,line,offset = open_file(args)
        text=arr[line+offset-1]
        
    elif key==keys["ctrl+t"]: ch_T_SP = not ch_T_SP

    else: #All the other keys
        if not str(key)[4:6] in fixstr:
            out=decode(key,getch);p1=text[:pointer-1]; p2=text[pointer-1:]
            if out=="\t" and ch_T_SP: out=" "*4; pointer+=3
            text=(p1+out+p2); pointer+=1; status_st=False

    return text,pointer,oldptr,line,offset,columns,banoff,arr,rows,max_len,filename,status,status_st,copy_buffer,fixstr,fix,ch_T_SP

