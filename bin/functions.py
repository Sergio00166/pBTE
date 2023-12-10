#Code by Sergio1260

from os import get_terminal_size
from sys import path
path.append(path[0]+"\\lib.zip")
from wcwidth import wcwidth

def wrap(text, columns):
    out=[]; counter=-1; buffer=""
    for x in text:
        if counter>=columns-1:
            if x=="\t":
                lenght=tab_len(text.index(x),text)
            else: lenght=wcwidth(x)
            if lenght>1: out.append(buffer)
            else: out.append(buffer+x)
            buffer=""; counter=0       
        else:
            buffer+=x
            if x=="\t": counter+=tab_len(text.index(x),text)
            else: counter+=wcwidth(x)
    if not buffer=="": out.append(buffer)
    return out

def decode(key):
    for x in range(3):
        try: out=key.decode("UTF-8"); break
        except: key+=getch()
    return out

def get_size():
    size=get_terminal_size()
    return size[1]-4,size[0]-2

def fix_arr_line_len(arr, columns, black, reset):
    out=[]
    for x in arr:
        bigger=text_real_size(x)>columns+1
        if bigger: out.append(x[:columns+1]+black+">"+reset)
        else: out.append(x)
    return out
      
def tab_len(pointer,text):
    fix=text[:pointer+1]+"\f"+text[pointer+1:]
    fix=fix.expandtabs(8); length=fix[pointer:]
    length=length[:length.find("\f")]   
    return len(length)

def text_real_size(text):
    lenght=0
    for x in text:
        if x=="\t": lenght+=tab_len(text.index(x),text)
        else: lenght+=wcwidth(x)
    return lenght

def fixlenline(text, pointer, oldptr):
    length=len(text)+1
    if pointer>length or oldptr>length:
        return length,oldptr
    elif oldptr>pointer: return oldptr,oldptr
    else: return pointer,oldptr
        
