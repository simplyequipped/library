@echo off
echo Offline Forum Utility
start /B kiwix-serve.exe --library library_forum.xml
start "" http://localhost/
pause
taskkill /F /IM kiwix-serve.exe