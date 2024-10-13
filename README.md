# pBTE
python-based Basic Text Editor

A a basic terminal text editor with python using the minimun external libraries as possible (only wcwidth and colorama) 
Only supports UTF-8 (normal mode) and ASCII (for reading bin files)

Using colorama and wcwidth (they are inside lib.zip) and its LICENSES can be found inside that zip file

Basic functionalities currently available such as copy, cut, paste lines, find string, and replaced string.
<br>Currently ctrl+Z is not available a workaround is using ctrl+a and then ctrl+b to create a .bak file
<br><br>
To see all options press F1 (Windows) or Ctrl+H (Linux) to show the extra controls (if available)

<h3>Requirements:</h3>
Python 3 (tested under python 3.13)<br>
No dependencies<br>
Windows or Linux with UTF-8 keyboard <br>

<h3>Issues</h3>
Due to limitations with msvcrt.getch() on windows to select (highlight) lines you must use Ctrl+arrows instead of Shift+arrows<br>
On linux some terminal emulators intercept Ctrl + PgUP and Ctrl + PgDown but we cannot
use Shift instead of Ctrl due to internal limitations on how the keystrokes is read. <br>

