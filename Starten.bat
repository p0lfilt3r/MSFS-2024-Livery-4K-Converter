@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MSFS_4K_Livery_Converter.py
if errorlevel 1 (
  echo.
  echo Das Programm konnte nicht gestartet werden.
  echo Bitte Python 3 installieren und danach Pillow mit folgendem Befehl:
  echo python -m pip install Pillow
  pause
)
