#!/usr/bin/env python3
# Code by Sergio00166

def update_screen_thread():
    """Thread function to continuously update screen dimensions"""
    global app_state, run_thread, kill
    
    while not kill:
        delay(0.01)
        if run_thread:
            # Save old dimensions and get new values
            old_rows = app_state.rows
            old_columns = app_state.columns
            app_state.rows, app_state.columns = get_size()
            
            # Check if terminal is too small
            if app_state.rows < 4 or app_state.columns < 24:
                print("\r\033cTerminal too small")
            # Check if dimensions changed
            elif old_rows != app_state.rows or old_columns != app_state.columns:
                # Adjust offset if line exceeds visible rows
                if app_state.line > app_state.rows:
                    app_state.offset += (app_state.line - app_state.rows)
                    app_state.line = app_state.rows
                
                # Restore TTY to default values on Linux
                if sep != chr(92):  # Not Windows
                    tcsetattr(fd, TCSADRAIN, old_settings)
                
                print("\r\033[3J")  # Clear previous content
                update_scr(app_state)
                
                # Set TTY to raw mode on Linux
                if sep != chr(92):  # Not Windows
                    setraw(fd, when=TCSADRAIN)


if __name__ == "__main__":
    from sys import path
    from os import sep
    
    # Add the bin folder to import path
    path.append(path[0] + sep + "bin")
    from init import *
    
    # Start the update thread
    update_thread = Thread(target=update_screen_thread)
    run_thread, kill = True, False
    update_thread.daemon = True
    update_thread.start()
    
    while True:
        # Ensure array is never empty
        if len(app_state.arr) == 0:
            app_state.arr = [""]
        
        # Get terminal size and update screen
        app_state.rows, app_state.columns = get_size()
        update_scr(app_state)
        
        # Pause update thread while waiting for key input
        run_thread = True
        key = getch()
        run_thread = False
        
        # Handle Ctrl+Q (quit) - open next file or exit
        if key == app_state.keys["ctrl+q"]:
            if len(files) > 0:
                # Try to open next file from queue
                for _ in range(len(files)):
                    try:
                        filename, files = files[0], files[1:]
                        read_UTF8(app_state, filename)
                        app_state.status_st = False
                        app_state.cursor, app_state.offset = 0, 0
                        app_state.line = app_state.banoff
                        break
                    except: pass
            else:
                kill = True
                update_thread.join()
                break
        
        # Process key input
        keys_func(app_state, key)
    
    # Restore TTY buffer and exit
    print("\x1b[?1049l", end="")
    exit(0)

