#Code by Sergio1260

           
if not __name__=="__main__":

    from msvcrt import getch
    from os import getcwd
    from sys import argv
    from os.path import exists
    from fixes import *
    from keys import keys
    from subprocess import check_output
    from colorama import init, Fore, Back, Style
    from threading import Thread
    from time import sleep as delay
    
    init(autoreset=False,convert=True); reset=Style.RESET_ALL
    black=Back.WHITE+Style.DIM+Fore.BLACK+Style.DIM
    
    version="v0.3.0"
    
    rows,columns=get_size()

    tab_len=8; tabchr=b'\xc2\xa0'.decode("UTF-8")
    ch_T_SP=False
    
    # FIXES WHEN USING LEGACY CMD
    fix_oldcmd=str(check_output("mode con", shell=True)).split("\\r\\n")[3].replace(" ","")
    fix_oldcmd=int(fix_oldcmd[fix_oldcmd.find(":")+1:])
    if fix_oldcmd>rows+4: legacy=True
    else: legacy=False
        
    #Check if we have arguments via cli, if not create an empty one
    if not len(argv)==1:
        filename=" ".join(argv[1:])

        #If file exist open it if not create an empty list
        if exists(filename): 
            tmp=open(filename, "r", encoding="UTF-8").readlines(); arr=[]
            for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
            arr=fix_read_tab(arr,tab_len,tabchr)
            arr.append("")
        else: arr=[""]
        
    else: #Create an empty new file
        filename="NewFile"; arr=[""] 

    if not ":\\" in filename: #Fix file path
        filename=getcwd()+"\\"+filename 

    # Creates a list of banned chars code
    values=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
    fixstr=[]
    for x in range(0,2):
        for y in values:
            fixstr.append(str(x)+y)
    
    #Define a lot of stuff
    text=arr[0]; pointer=offset=0; line=banoff=1
    banner=black+" "*3+"pBTE "+version+reset
    bottom="\n\n    "+black+"^Q"+reset+" EXIT  "+black+"^S"+reset+" SAVE  "
    bottom+=black+"^A"+reset+" Save as  "+black+"^O"+reset+" OPEN  "
    bottom+=black+"^C"+reset+" COPY  "+black+"^X"+reset+" CUT  "
    bottom+=black+"^P"+reset+" PASTE  "+black+"^G"+reset+" GOTO  "
    bottom+=black+"^T"+reset+" T/SP    "
    copy_buffer=""; fix=False; oldptr=0; p_offset=0

    #Flag to show after saving the file
    saved_txt=black+"SAVED"+reset; status=saved_df=black+" "*5+reset; status_st=0

    

    

