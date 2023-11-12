#Code by Sergio1260

if not __name__=="__main__":
    from msvcrt import getch
    from os import get_terminal_size, getcwd
    from sys import argv
    from os.path import exists
    from functions1 import *
    from functions2 import *

    version="v0.1.8"

    #Check if we have arguments via cli, if not ask the user for a file to open
    if not len(argv)==1: filename=" ".join(argv[1:])
    else: filename=str(input("File to open: "))
    if not ":\\" in filename: filename=getcwd()+"\\"+filename

    #If file exist open it if not create an empty list
    if exists(filename): 
        tmp=open(filename, "r", encoding="UTF-8").readlines(); arr=[]
        for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
        arr.append("")
    else: arr=[""]

    #Define a lot of stuff
    text=arr[0]; pointer=offset=0; line=banoff=1
    black="[47m[30m[2m"; reset="[0m"; rows=get_terminal_size()[1]-4
    banner="█"*8+black+"pBTE "+version+reset
    bottom="\n\n\t"+black+"^Q"+reset+" EXIT    "+black+"^S"+reset+" SAVE    "
    bottom+=black+"^A"+reset+" Save as    "+black+"^X"+reset+" CUT    "
    bottom+=black+"^C"+reset+" COPY    "+black+"^P"+reset+" PASTE    "
    bottom+=black+"^G"+reset+" GOTO    "
    copy_buffer=""; cls="\033c"; fix=False; oldptr=0

    #Flag to show after saving the file
    saved_txt=black+"SAVED"+reset; status=saved_df="█"*5; status_st=0

    p_offset=0; columns=get_terminal_size()[0]-2

