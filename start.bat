@echo off


:a
git reset --hard
git fetch
git pull

taskkill /f /im python.exe

start /B py scrapper.py> log.txt
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