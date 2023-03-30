@echo off
if exist "./running.bat" (
    running.bat
    del running.bat
)
python trackcopy.py
