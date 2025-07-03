@echo off
setlocal ENABLEDELAYEDEXPANSION
set "PY_CMD="
set "PY_VER="

for /f "tokens=2 delims= " %%v in ('python --version 2^>nul') do (
    set "PY_VER=%%v"
    for /f "tokens=1,2 delims=." %%a in ("%%v") do (
        set /a MAJOR=%%a
        set /a MINOR=%%b
        if !MAJOR! GEQ 3 if !MINOR! GEQ 10 (
            set "PY_CMD=python"
            goto :found
        )
    )
)

for %%C in ("py -3.13" "py -3.12" "py -3.11" "py -3.10") do (
    %%~C --version >nul 2>&1
    if not errorlevel 1 (
        set "PY_CMD=%%~C"
        goto :found
    )
)

echo [!] No suitable Python 3.10+ interpreter found.
pause
exit /b 1

:found
echo [*] Using Python command: %PY_CMD%

set VENV_DIR=.venv
if not exist %VENV_DIR%\Scripts\python.exe (
    echo [*] Creating virtual environment...
    %PY_CMD% -m venv %VENV_DIR%
    %VENV_DIR%\Scripts\python.exe -m pip install --upgrade pip
    %VENV_DIR%\Scripts\python.exe -m pip install -r requirements.txt
    echo * > %VENV_DIR%\.gitignore
)

echo [*] Launching app...
start "" %VENV_DIR%\Scripts\pythonw.exe main.pyw
