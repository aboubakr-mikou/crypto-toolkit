@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    py -m venv .venv
    if errorlevel 1 goto fail
)
if not exist ".venv\installed-v2" (
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto fail
    type nul > ".venv\installed-v2"
)
".venv\Scripts\python.exe" main.py
if errorlevel 1 goto fail
exit /b 0
:fail
echo Launch failed. Check Python 3.10+ installation and dependencies.
pause
exit /b 1
