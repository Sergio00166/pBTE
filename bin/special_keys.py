#Code by Sergio1260

from msvcrt import getch
from functions1 import *

def special_keys(pointer,text,columns,offset,line,banoff,arr,rows,oldptr,max_len,status_st):
    
    special_key=getch() #Read char
    
    if special_key==b'H': #Up
        pointer, oldptr, text, offset, line =\
        up(line,offset,arr,text,banoff,oldptr,rows,pointer)

    elif special_key==b'P': #Down
        pointer, oldptr, text, offset, line =\
        down(line,offset,arr,text,banoff,oldptr,rows,pointer)

    elif special_key==b'M': #Right
        text, pointer, oldptr, line, offset =\
        right(pointer,text,columns,offset,line,banoff,arr,rows,oldptr)
            
    elif special_key==b'K': #Left
        pointer, oldptr, text, line, offset =\
        left(pointer,oldptr,line,offset,banoff,text,arr)
        
    elif special_key==b'S': #Supr
        text,arr = supr(pointer,max_len,text,offset,banoff,arr,line)
        status_st=False

    elif special_key==b'G': #Start
        pointer=1; p_offset=0
        oldptr=pointer
    
    elif special_key==b'O': #End
        pointer=len(text)+1
        oldptr=pointer

    return text, pointer, oldptr, line, offset, status_st

