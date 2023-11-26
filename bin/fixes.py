#Code by Sergio1260

from msvcrt import getch
from os import get_terminal_size


def fix_read_tab(arr,tab_len,tabchr):
    new_arr=[]
    for x in arr:
        x=x.replace(" ","\n")
        x=x.expandtabs(tab_len)
        x=x.replace(" ",tabchr)
        x=x.replace("\n"," ")
        new_arr.append(x)
    return new_arr

def fix_out_tab(arr,tabchr,tab_len):
    for x in arr:
        text=x
        while tabchr in text:
            p1=text[:text.find(tabchr)]
            p2=text[text.find(tabchr)+1:]
            for y in range(tab_len):
                if not len(p2)==0 and p2[0]==tabchr:
                    p2=p2[1:]
            text=p1+"\t"+p2
        arr[arr.index(x)]=text
    return arr

def fix_tab(pointer,text,tab_len):
    p1=text[:pointer+1]
    p2=text[pointer+1:]
    fix=p1+"\f"+p2
    fix=fix.expandtabs(tab_len)
    length=fix[pointer:]
    length=length[:length.find("\f")]
              
    return len(length)

def decode(key):
    for x in range(3):
        try: out=key.decode("UTF-8"); break
        except: key+=getch()
    return out

def get_size():
    size=get_terminal_size()
    return size[1]-4,size[0]-2

def update_scr(black,reset,legacy,status,p_offset,banoff,offset,line,pointer,arr,banner,filename,bottom,rows,columns):
    position=black+"  "+str(line+offset-banoff)+" "*(4-len(str(line+offset-banoff)))
    all_file=fix_scr(arr[offset:rows+offset+1], arr, p_offset, black, reset, columns, line, offset, banoff)
    outb=position+black+" "+reset+status+banner
    if not legacy: cls="\033c"
    else: cls=("\r\033[%d;%dH"%(rows+4, columns+2))+"\n"
    print(cls+outb+black+" "*(columns-27-len(filename))+reset, end="")
    print(black+filename+reset+black+" "+reset+"\n"+all_file, end="")
    print("\n"*(rows-len(arr)+1)+bottom+("\r\033[%d;%dH"%(line+1, pointer)), end="")

def fix_scr(arr, org_arr, p_offset, black, reset, columns, line, offset, banoff):
    out=[]
    for x in arr: out.append(fix_line(x, 0, black, reset, columns))
    x=org_arr[line+offset-banoff]
    try:
        out[line-banoff]=fix_line(x, p_offset, black, reset, columns)
        return "\n".join(out)
    except:
        out.append(fix_line(x, p_offset, black, reset, columns))
        return "\n".join(out[1:])

def fix_line(text, p_offset, black, reset, columns):
    if len(text)>columns:
        if p_offset < 0: p_offset = 0
        if p_offset + columns > len(text): p_offset = len(text) - columns+1
        fix_text = text[p_offset:p_offset + columns]
        if p_offset > 0: fix_text=black+'<'+reset+fix_text[1:]
        if p_offset+columns<len(text): fix_text=fix_text[:-1]+black+'>'+reset
    else: fix_text=text
    return fix_text

def fixlenline(text, pointer, oldptr, p_offset):
    if p_offset+pointer>len(text)+2: p_offset=0
    length=len(text)+1
    if pointer>length or oldptr>length:
        return length,oldptr,p_offset
    elif oldptr>pointer: return oldptr,oldptr,p_offset
    else: return pointer,oldptr,p_offset

