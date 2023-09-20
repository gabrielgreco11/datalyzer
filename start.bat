@echo off
start /B python main.py
:a
git fetch
git pull
:loop
timeout /t 1 /nobreak > NULL
if exist "restart" (
    DEL restart
    echo Found 'restart' file. Exiting...
    taskkill /f /im python.exe
    goto a
)
goto loop