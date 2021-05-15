@echo off
cd %~dp0
cd ..
cd ..

if exist %cd%\FriendRatingServer\venv\Scripts\activate.bat (
    call "%cd%\FriendRatingServer\venv\Scripts\activate.bat"
    call "%cd%\FriendRatingServer\windows_script\run_server_func.bat"
) else (
    call "%cd%\FriendRatingServer\windows_script\run_server_func.bat"
)
