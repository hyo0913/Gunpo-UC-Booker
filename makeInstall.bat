pyside6-uic MainForm.ui -o ui_MainForm.py
pyside6-uic BookItemForm.ui -o ui_BookItemForm.py

pyinstaller MainForm.py --noconsole --onefile -i icon.ico -n "GunpoUcBooker.exe" --add-data ui_*.py;.

pause