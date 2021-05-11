switch (echo $PYTHONPATH | grep FriendRatingServer1)
    case ""
        set -ax PYTHONPATH $PWD
end

python ./friend_rating_server/manage.py runserver localhost:8000