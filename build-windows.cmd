@echo off
cd /d "%~dp0"
py -3 -m pip install pyinstaller==6.12.0 || exit /b 1
py -3 -m PyInstaller --noconfirm --clean --onefile --windowed --name PugCrypt desktop.py
