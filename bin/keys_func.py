#Code by Sergio1260

from functions import *
from actions import *
from actions1 import *
from saveas import save_as
from openfile import open_file

def keys_func(key,text,pointer,oldptr,line,offset,columns,banoff,arr,rows,
              max_len,filename,status,status_st,copy_buffer,fixstr,fix,\
              black,reset,saved_txt,ch_T_SP,banner,getch,keys,select):
        
    if key==keys["special"]:
        if not sep==chr(92): getch()
        special_key=getch() #Read char
        fix=(sep==chr(92) or special_key==b'1')
        if not sep==chr(92) and special_key==b'1':
            getch(); getch(); special_key=getch()

        if special_key==keys["supr"]:
            args=(pointer,max_len,text,offset,banoff,arr,line,select)
            text, arr, line, offset, select = supr(*args)
            if not sep==chr(92): getch()
            status_st = False
            
        # Not implemented yet
        elif special_key==keys["insert"] and (not sep==chr(92)): getch()

        elif special_key==keys["arr_up"] or special_key==keys["ctrl+arr_up"]:
            args=(line,offset,arr,text,banoff,oldptr,rows,pointer,special_key,keys,select,fix)
            pointer,oldptr,text,offset,line,select = up(*args)
            
        elif special_key==keys["arr_down"] or special_key==keys["ctrl+arr_down"]:
            args=(line,offset,arr,text,banoff,oldptr,rows,pointer,special_key,keys,select,fix)
            pointer, oldptr, text, offset, line, select = down(*args)

        elif special_key==keys["arr_right"] or special_key==keys["ctrl+arr_right"]:
            args=(pointer,text,columns,offset,line,banoff,arr,rows,oldptr)
            text,pointer,oldptr,line,offset = right(*args)
            select=[]
            
        elif special_key==keys["arr_left"] or special_key==keys["ctrl+arr_left"]:
            args=(pointer,oldptr,line,offset,banoff,text,arr)
            pointer,oldptr,text,line,offset = left(*args)
            select=[]
            
        elif special_key==keys["start"]:
            pointer=1; p_offset=0; oldptr=pointer; select=[]
            
        elif special_key==keys["end"]:
            pointer=len(text)+1; oldptr=pointer; select=[]
            
        elif special_key==keys["repag"]:
            args=(line,offset,banoff,rows,arr,sep,pointer,oldptr)
            line,offset,text,pointer,oldptr = repag(*args)
            if not sep==chr(92): getch()
            select=[]
            
        elif special_key==keys["avpag"]:
            args=(line,offset,banoff,rows,arr,sep,pointer,oldptr)
            line,offset,text,pointer,oldptr = avpag(*args)
            if not sep==chr(92): getch()
            select=[]

    elif key==keys["delete"]:
        args=(pointer,text,offset,line,arr,banoff,select)
        line,offset,text,arr,pointer,select = backspace(*args)
        status_st = False

    elif key==keys["return"]:
        args=(text,pointer,offset,banoff,line,arr,rows,status,select)
        line,offset,arr,pointer,text,staus,select = newline(*args)
        status_st = False

    elif key==keys["ctrl+s"]:
        out=open(filename,"w",encoding="UTF-8")
        out.write("\n".join(arr)); out.close()
        status=saved_txt; status_st=True
        out=open(filename,"r",encoding="UTF-8")
        
    elif key==keys["ctrl+x"]:
        args=(select,arr,line,offset,banoff,text,status_st,copy_buffer,pointer)
        copy_buffer,arr,text,line,offset,select = cut(*args)
        
    elif key==keys["ctrl+c"]:
        args=(select,arr,line,offset,banoff,pointer)
        copy_buffer,select = copy(*args)
        
    elif key==keys["ctrl+p"]:
        args=(copy_buffer,arr,line,offset,banoff,pointer,text,status_st)
        pointer,arr,text,status_st,copy_buffer = paste(*args)                                              
            
    elif key==keys["ctrl+g"]:
        args=(columns,rows,banoff,line,arr,offset,black)
        line,offset,text = goto(*args)

    elif key==keys["ctrl+a"]:
        args = (filename,black,reset,rows,banoff,arr,columns,status,offset,line,banner,status_st,saved_txt,getch,keys,fixstr)
        status_st,filename,status = save_as(args)

    elif key==keys["ctrl+o"]:
        args = (filename,black,reset,rows,banoff,arr,columns,status,offset,line,banner,status_st,getch,keys,pointer,fixstr)
        arr,filename,status_st,pointer,line,offset = open_file(args)
        text=arr[line+offset-1]
        
    elif key==keys["ctrl+t"]: ch_T_SP = not ch_T_SP

    else: #All the other keys
        if not str(key)[4:6] in fixstr:
            if not len(select)==0:
                select,arr,text,line,offset =\
                del_sel(select, arr, banoff)
            out=decode(key,getch)
            p1, p2 = text[:pointer-1], text[pointer-1:]
            if out=="\t" and ch_T_SP: out=" "*4; pointer+=3
            text=(p1+out+p2); pointer+=1; status_st=False

    return text,pointer,oldptr,line,offset,columns,banoff,arr,rows,max_len,\
           filename,status,status_st,copy_buffer,fixstr,fix,ch_T_SP,select

