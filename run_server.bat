@echo off
set var=%cd%
cd %~dp0
cd ..

if exist %cd%\FriendRatingServer\venv\Scripts\activate.bat (
    %cd%\FriendRatingServer\venv\Scripts\activate.bat
    if "%PYTHONPATH%" == "" (
        set PYTHONPATH=%cd%\FriendRatingServer
    ) else (
        set PYTHONPATH=%PYTHONPATH%;%cd%\FriendRatingServer
    )
    cd FriendRatingServer
    python friend_rating_server/manage.py collectstatic
    python friend_rating_server/manage.py migrate
    python friend_rating_server/manage.py runserver localhost:8000
) else (
    if "%PYTHONPATH%" == "" (
        set PYTHONPATH=%cd%\FriendRatingServer
    ) else (
        set PYTHONPATH=%PYTHONPATH%;%cd%\FriendRatingServer
    )
    cd FriendRatingServer
    python friend_rating_server/manage.py collectstatic
    python friend_rating_server/manage.py migrate
    python friend_rating_server/manage.py runserver localhost:8000
)
