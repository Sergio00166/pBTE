#Code by Sergio1260

from msvcrt import getch
from functions1 import *
from functions2 import *

def special_keys(pointer,p_offset,text,columns,offset,line,banoff,arr,rows,oldptr,max_len,status_st,tabchr,tab_len):
    
    special_key=getch() #Read char
    
    if special_key==b'H': #Up
        pointer, oldptr, text, offset, line, p_offset =\
        up(line,offset,arr,text,banoff,oldptr,rows,pointer,p_offset)

    elif special_key==b'P': #Down
        pointer, oldptr, text, offset, line, p_offset =\
        down(line,offset,arr,text,banoff,oldptr,rows,pointer,p_offset)

    elif special_key==b'M': #Right
        text, pointer, p_offset, oldptr, line, offset =\
        right(pointer,p_offset,text,columns,offset,line,\
              banoff,arr,rows,oldptr,tabchr,tab_len)
            
    elif special_key==b'K': #Left
        pointer, oldptr, p_offset, text, line, offset =\
        left(pointer,oldptr,line,offset,banoff,columns,\
             p_offset,text,arr,tabchr,tab_len)
        
    elif special_key==b'S': #Supr
        text,arr = supr(pointer,max_len,text,offset,banoff,arr,line,p_offset,tabchr,tab_len)
        status_st=False

    elif special_key==b'G': #Start
        pointer=1; p_offset=0
        oldptr=pointer
    
    elif special_key==b'O': #End
        if len(text)>columns+1: p_offset=len(text)-columns+2; pointer=columns
        else: pointer=len(text)+1
        oldptr=pointer

    return text, pointer, p_offset, oldptr, line, offset, status_st

