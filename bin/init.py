#Code by Sergio1260

           
if not __name__=="__main__":

    from os import getcwd, sep
    from sys import argv, path
    from os.path import exists, isabs
    from functions import get_size
    from upd_scr import update_scr
    from keys_func import keys_func
    from subprocess import check_output
    path.append(path[0]+sep+"lib.zip")
    from colorama import init, Fore, Back, Style, deinit
    from threading import Thread
    from time import sleep as delay
    from time import time
    
    init(autoreset=False,convert=True); reset=Style.RESET_ALL
    black=Back.WHITE+Style.DIM+Fore.BLACK+Style.DIM; deinit()
    rows,columns=get_size(); ch_T_SP=False
    
    version="v0.4.9.8"
    
    if sep==chr(92): #Windows
        from msvcrt import getch
    else: # Unix like OSes
        import sys; import tty; import termios
        def getch():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                char = sys.stdin.read(1).encode('utf-8')
            finally: termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return char
    
    #Check if we have arguments via cli, if not create an empty one
    if not len(argv)==1:
        filename=" ".join(argv[1:])

        #If file exist open it if not create an empty list
        if exists(filename): 
            tmp=open(filename, "r", encoding="UTF-8").readlines(); arr=[]
            for x in tmp: arr.append(x.replace("\r","").replace("\n","").replace("\f",""))
            arr.append("")
        else: arr=[""]
        
    else: #Create an empty new file
        filename="NewFile"; arr=[""] 

    if not isabs(filename): #Fix file path
        filename=getcwd()+sep+filename 

    # Creates a list of banned chars code
    values=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
    fixstr=[]
    for x in range(0,2):
        for y in values:
            fixstr.append(str(x)+y)
    
    #Define a lot of stuff
    text=arr[0]; pointer=offset=0; line=banoff=1
    banner=black+" "*3+"pBTE "+version+reset
    copy_buffer=""; fix=False; oldptr=p_offset=0

    #Flag to show after saving the file
    saved_txt=black+"SAVED"+reset; status=saved_df=black+" "*5+reset; status_st=0

    print("\033c", end=""); end=1; start=0

    if sep==chr(92):
        keys = {"special":b'\xe0',"delete":b'\x08',"return":b'\r',"ctrl+s":b'\x13',
                "ctrl+n":b'\x0e',"ctrl+x":b'\x18',"ctrl+c":b'\x03',"ctrl+p":b'\x10',
                "ctrl+g":b'\x07',"ctrl+a":b'\x01',"ctrl+o":b'\x0f',"ctrl+t":b'\x14',
                "ctrl+b":b'\x02',"ctrl+q":b'\x11',"arr_up":b'H',"arr_down":b'P',
                "arr_right":b'M',"arr_left":b'K',"supr":b'S',"start":b'G',
                "end":b'O',"repag":b'I',"avpag":b'Q',"tab":b'\t'}
    else:
        keys = {"special":b'\x1b',"delete":b'\x7f',"return":b'\r',"ctrl+s":b'\x13',
                "ctrl+n":b'\x0e',"ctrl+x":b'\x18',"ctrl+c":b'\x03',"ctrl+p":b'\x10',
                "ctrl+g":b'\x07',"ctrl+a":b'\x01',"ctrl+o":b'\x0f',"ctrl+t":b'\x14',
                "ctrl+b":b'\x02',"ctrl+q":b'\x11',"arr_up":b'A',"arr_down":b'B',
                "arr_right":b'C',"arr_left":b'D',"supr":b'3',"start":b'1',
                "end":b'4',"repag":b'5',"avpag":b'6',"tab":b'\t'}

    

    

    

