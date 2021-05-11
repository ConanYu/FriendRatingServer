#!/bin/bash
this_dir=`pwd`
dirname $0|grep "^/" >/dev/null
if [ $? -eq 0 ];then
  this_dir=`dirname $0`
else
  dirname $0|grep "^\." >/dev/null
  retval=$?
  if [ $retval -eq 0 ];then
    this_dir=`dirname $0|sed "s#^.#$this_dir#"`
  else
    this_dir=`dirname $0|sed "s#^#$this_dir/#"`
  fi
fi

if ["$PYTHONPATH" == ""]; then
  export PYTHONPATH=$this_dir
else
  export PYTHONPATH=$PYTHONPATH:$this_dir
fi

ip=`ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"`

python "$this_dir/friend_rating_server/manage.py" collectstatic
python "$this_dir/friend_rating_server/manage.py" migrate
python "$this_dir/friend_rating_server/manage.py" runserver $ip:9988
