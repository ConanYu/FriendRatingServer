@echo off
cd %~dp0
cd ..

RMDIR /S /Q static
mkdir static
xcopy "%cd%\friend_rating_server\static\*" "%cd%\static" /e /i
