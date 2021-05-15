@echo off
if "%PYTHONPATH%" == "" (
    set PYTHONPATH=%cd%\FriendRatingServer
) else (
    set PYTHONPATH=%PYTHONPATH%;%cd%\FriendRatingServer
)
cd FriendRatingServer
RMDIR /S /Q static
python friend_rating_server/manage.py collectstatic
python friend_rating_server/manage.py runserver localhost:8000
