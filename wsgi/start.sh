#!/bin/sh
#TODO: if logs/wsgi.pid exists exit

E_NO_ARGS=65

if [ $# -eq 0 ]
then
  echo "Must specify an IP address."
  exit $E_NO_ARGS
fi  

./manage.py runwsgi --host $1 -d start
