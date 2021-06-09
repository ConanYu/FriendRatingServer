cd (dirname (status --current-filename))
cd ..
set python_path (echo $PYTHONPATH | grep FriendRatingServer)
switch (echo $python_path)
    case ""
        set -ax PYTHONPATH $PWD
end

pip3 install -r requirements.txt
python3 friend_rating_server/manage.py collectstatic
python3 ./friend_rating_server/manage.py runserver localhost:8000