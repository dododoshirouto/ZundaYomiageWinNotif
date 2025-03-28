@echo on

echo This app does not run on building exe.
@REM pause
@REM exit

set APP_NAME=zundamon_yomiage_win_notif

if exist dist\%APP_NAME% (
    rmdir /s /q dist\%APP_NAME%
)

    @REM --noconsole ^
"venv\Scripts\python.exe" -m PyInstaller --onedir ^
    --name "%APP_NAME%" ^
    --icon "icon.ico" ^
    --noconsole ^
    --add-data "model/*;voicevox_core/model"^
    --add-data "open_jtalk_dic_utf_8-1.11;open_jtalk_dic_utf_8-1.11"^
    --add-data "bep-eng.dic.txt;."^
    --add-data "cmudict-0.7b_baseform;."^
    --add-data "assets;assets"^
    _main.py

dist\%APP_NAME%\%APP_NAME%.exe

pause