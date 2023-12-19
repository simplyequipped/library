@echo off
echo Offline Reference Utility
start /B kiwix-serve.exe --library library_reference.xml
start "" http://localhost/
pause
taskkill /F /IM kiwix-serve.exe