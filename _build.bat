set APP_NAME=zundamon_yomiage_win_notif

if exist dist\%APP_NAME%.exe (
    remove dist\%APP_NAME%.exe
)

    @REM --noconsole ^
"venv\Scripts\python.exe" -m PyInstaller --onefile ^
    --name "%APP_NAME%" ^
    --icon "icon.ico" ^
    --add-data "assets/standby.png;assets" ^
    --add-data "assets/talking.png;assets" ^
    --add-data "assets/talking_2.png;assets" ^
    --add-data "assets/talking_3.png;assets" ^
    --add-data "assets/sleep.png;assets" ^
    --add-data "assets/sleep_2.png;assets" ^
    --add-data "bep-eng.dic.txt;." ^
    --add-data "model/metas.json;model" ^
    _main.py

pause