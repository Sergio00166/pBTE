#Code by Sergio1260

from actions import up, down, right, left, supr
from os import sep

def special_keys(pointer,text,columns,offset,line,banoff,arr,rows,oldptr,max_len,status_st,getch,keys):

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
        
    elif special_key==keys["supr"]: #Supr
        text,arr = supr(pointer,max_len,text,offset,banoff,arr,line)
        status_st=False

    elif special_key==keys["start"]: #Start
        pointer=1; p_offset=0
        oldptr=pointer
    
    elif special_key==keys["end"]: #End
        pointer=len(text)+1
        oldptr=pointer

    return text, pointer, oldptr, line, offset, status_st

