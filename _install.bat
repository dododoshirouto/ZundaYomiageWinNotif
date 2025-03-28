@echo on

@REM install python if not exist
set PYTHON=python
where /q %PYTHON% --version
if %errorlevel% <> 0 (
    echo install python...
    curl -o python.zip https://www.python.org/ftp/python/3.12.2/python-3.12.2-embed-amd64.zip
    mkdir python-3.12.2
    tar -xf python.zip -C python-3.12.2\
    del python.zip
    set PATH="%~dp0python-3.12.2;%PATH%"
)

IF NOT EXIST venv\Scripts\activate (
    echo create venv...
    %PYTHON% -m venv venv
) ELSE (
    echo venv is exists.
)

echo install python modules...
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
    echo install voicevox...
    voicevox-download-windows-x64.exe -v %VOICEVOX_VERSION% -o ./
) ELSE (
    echo voicevox is installed.
)

IF NOT EXIST venv\Lib\site-packages\voicevox_core (
    echo install voicevox_core modules...
    "venv\Scripts\python.exe" -m pip install https://github.com/VOICEVOX/voicevox_core/releases/download/%VOICEVOX_VERSION%/voicevox_core-%VOICEVOX_VERSION%+cpu-cp38-abi3-win_amd64.whl
) ELSE (
    echo voicevox_core modules is installed.
)

@REM download The CMU Pronouncing Dictionary

IF NOT EXIST cmudict-0.7b_baseform (
    echo Downloading cmudict-0.7b_baseform...
    set PERL=perl
    where /q %PERL% --version
    if %errorlevel% <> 0 (
        echo install perl...
        curl -L -o strawberry-perl-5.40.0.1-64bit-portable.zip https://github.com/StrawberryPerl/Perl-Dist-Strawberry/releases/download/SP_54001_64bit_UCRT/strawberry-perl-5.40.0.1-64bit-portable.zip
        echo unzip...
        mkdir strawberry-perl
        tar -xf strawberry-perl-5.40.0.1-64bit-portable.zip -C strawberry-perl\
        del strawberry-perl-5.40.0.1-64bit-portable.zip
        set PATH="%CD%\strawberry-perl\perl\bin;%PATH%"
    )
    echo download cmudict-0.7b...
    curl -L -o cmudict-0.7b http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b
    curl -L -o make_baseform.pl http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/scripts/make_baseform.pl
    %PERL% make_baseform.pl cmudict-0.7b cmudict-0.7b_baseform
) ELSE (
    echo cmudict-0.7b_baseform is exists.
)

pause