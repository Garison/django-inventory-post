#!/bin/sh
PID=`ps x a | grep 'runwsgi' | cut -d?  -f1`
if [ -z $PID ]
then
  echo "wsgi is not running."
  exit 0
fi

echo "PID: $PID"
sudo kill $PID
rm logs/wsgi.pid
