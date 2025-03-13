set APP_NAME=zundamon_yomiage_win_notif

if exist dist\%APP_NAME%.exe (
    remove dist\%APP_NAME%.exe
)

"venv\Scripts\python.exe" -m PyInstaller --onefile ^
    --noconsole ^
    --name "%APP_NAME%" ^
    --icon "icon.ico" ^
    _main.py
pause