@echo off
set var=%cd%
cd %~dp0
cd ..
if "%PYTHONPATH%" == "" (
    set PYTHONPATH=%cd%\FriendRatingServer
) else (
    set PYTHONPATH=%PYTHONPATH%;%cd%\FriendRatingServer
)
cd FriendRatingServer
python friend_rating_server/manage.py runserver localhost:8000
