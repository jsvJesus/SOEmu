@echo off
setlocal
cd /d "%~dp0server"
echo Checking Python dependencies: cryptography, PyMySQL...
python -c "import cryptography, pymysql" >nul 2>nul
if errorlevel 1 (
    echo Installing server dependencies...
    python -m pip install -r "..\requirements.txt"
    if errorlevel 1 (
        echo.
        echo ERROR: Could not install server dependencies.
        echo Run manually: python -m pip install -r requirements.txt
        pause
        exit /b 1
    )
)
echo.
echo Starting SOEmulator with MariaDB persistence...
python so_emulator.py %*
if errorlevel 1 (
    echo.
    echo SOEmulator exited with an error.
    pause
)
endlocal
