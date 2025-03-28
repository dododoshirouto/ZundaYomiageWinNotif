@echo on

echo This app does not run on building exe.
@REM pause
@REM exit

set APP_NAME=zundamon_yomiage_win_notif

if exist dist\%APP_NAME%.exe (
    rmdir /s /q dist\%APP_NAME%.exe
)

    @REM --noconsole ^
"venv\Scripts\python.exe" -m PyInstaller^
    --onefile ^
    --name "%APP_NAME%" ^
    --icon "icon.ico" ^
    --add-data "model/*;voicevox_core/model"^
    --add-data "open_jtalk_dic_utf_8-1.11;open_jtalk_dic_utf_8-1.11"^
    --add-data "bep-eng.dic.txt;."^
    --add-data "cmudict-0.7b_baseform;."^
    --add-data "assets;assets"^
    _main.py

dist\%APP_NAME%.exe

:pause


goto :endmemo
:memo
voicevox models
pd0.bin
pi0.bin
d0.bin
    ずんだもん
    四国めたん
    春日部つむぎ
    雨晴はう
pd2.bin
pi2.bin
d2.bin
    九州そら
    九州そら_ささやき
pd8.bin
pi8.bin
d8.bin
    WhiteCUL
pd6.bin
pi6.bin
d6.bin
    No.7
    No_7_読み聞かせ
pd3.bin
pi3.bin
d3.bin
    中国うさぎ
pd14.bin
pi14.bin
d14.bin
    栗田まろん
pd5.bin
pi5.bin
d5.bin
    四国めたん_ヒソヒソ
    ずんだもん_ヒソヒソ


:endmemo