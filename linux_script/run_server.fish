cd (dirname (status --current-filename))
cd ..
switch (echo $PYTHONPATH | grep FriendRatingServer)
    case ""
        set -ax PYTHONPATH $PWD
end

python friend_rating_server/manage.py collectstatic
python ./friend_rating_server/manage.py runserver localhost:8000