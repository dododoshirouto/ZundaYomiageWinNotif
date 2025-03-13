@echo off

set VOICEVOX_VERSION=0.15.7

IF NOT EXIST voicevox-download-windows-x64.exe (
    echo Downloading download-windows-x64.exe from voicevox_core ...
    curl -L -o voicevox-download-windows-x64.exe https://github.com/VOICEVOX/voicevox_core/releases/download/%VOICEVOX_VERSION%/download-windows-x64.exe
)

IF NOT EXIST voicevox_core.dll (
    voicevox-download-windows-x64.exe -v %VOICEVOX_VERSION% -o ./
)

IF NOT EXIST venv\Scripts\activate (
    _install
)

venv\Scripts\python -m pip install https://github.com/VOICEVOX/voicevox_core/releases/download/%VOICEVOX_VERSION%/voicevox_core-%VOICEVOX_VERSION%+cpu-cp38-abi3-win_amd64.whl