@echo off


:a
git fetch
git pull

start /B py scrapper.py
start /B py main.py > log.txt

:loop
timeout /t 1 /nobreak > NULL
if exist "restart" (
    DEL restart
    echo Found 'restart' file. Exiting...
    taskkill /f /im python.exe
    goto a
)
goto loop