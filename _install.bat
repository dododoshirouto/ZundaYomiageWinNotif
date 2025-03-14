@echo off

IF NOT EXIST venv\Scripts\activate (
    echo create venv.
    python -m venv venv
) ELSE (
    echo venv is exists.
)

echo install python modules.
"venv\Scripts\python.exe" -m pip install -r requirements.txt

set VOICEVOX_VERSION=0.15.7
echo VOICEVOX_VERSION is %VOICEVOX_VERSION%.

@REM download and install voicevox_core

IF NOT EXIST voicevox-download-windows-x64.exe (
    echo Downloading download-windows-x64.exe from voicevox_core ...
    curl -L -o voicevox-download-windows-x64.exe https://github.com/VOICEVOX/voicevox_core/releases/download/%VOICEVOX_VERSION%/download-windows-x64.exe
) ELSE (
    echo voicevox-download-windows-x64.exe is exists.
)

IF NOT EXIST voicevox_core.dll (
    echo install voicevox.
    voicevox-download-windows-x64.exe -v %VOICEVOX_VERSION% -o ./
) ELSE (
    echo voicevox is installed.
)

IF NOT EXIST venv\Lib\site-packages\voicevox_core (
    echo install voicevox_core modules.
    "venv\Scripts\python.exe" -m pip install https://github.com/VOICEVOX/voicevox_core/releases/download/%VOICEVOX_VERSION%/voicevox_core-%VOICEVOX_VERSION%+cpu-cp38-abi3-win_amd64.whl
) ELSE (
    echo voicevox_core modules is installed.
)

pause