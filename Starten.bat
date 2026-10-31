@echo off
chcp 65001 >nul
cd /d "%~dp0"
python MSFS_4K_Livery_Converter.py
if errorlevel 1 (
  echo.
  echo Das Programm konnte nicht gestartet werden / The application could not be started.
  echo Bitte Python 3 installieren und danach Pillow installieren / Please install Python 3 and then Pillow:
  echo python -m pip install -r requirements.txt
  pause
)
