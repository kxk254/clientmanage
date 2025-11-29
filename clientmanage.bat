@ECHO OFF
@REM start cmd.exe /K "cd /D C:\Users\konno\OneDrive - SCM\Dev && 1\Scripts\activate"
@REM start cmd.exe /K "cd /D C:\Users\konno\OneDrive - SCM\Dev\deployed\clientmanage && py manage.py runserver"
start cmd.exe /K "cd /D C:\Users\konno\OneDrive - SCM\Dev && 1\Scripts\activate && cd /D C:\Users\konno\OneDrive - SCM\Dev\deployed\clientmanage && py manage.py runserver"
@REM del /S /Q "C:\Users\konno\AppData\Local\Google\Chrome\User Data\Default\Cache\*"
@REM for /D %%p in ("C:\Users\konno\AppData\Local\Google\Chrome\User Data\Default\Cache\*") do rmdir /S /Q "%%p"
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" "http://127.0.0.1:8000"
