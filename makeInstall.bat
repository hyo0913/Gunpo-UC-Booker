pyside6-uic MainForm.ui --rc-prefix -o ui_MainForm.py
pyside6-uic BookItemForm.ui --rc-prefix -o ui_BookItemForm.py

pyinstaller MainForm.py --noconsole --onefile -i icon.ico -n "GunpoUcBooker.exe"

pause