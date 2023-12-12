#!/bin/bash
set -e
LOGFILE=/var/log/gunicorn/hello.log
LOGDIR=/var/log/gunicorn/
NUM_WORKERS=3
TIME_OUT=30
# user/group to run as
USER=root
GROUP=root
cd /srv/www/app/
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn SkillSetGo.wsgi:application \
    -b 0.0.0.0:8000 -w $NUM_WORKERS -t $TIME_OUT \
    --user=$USER --group=$GROUP \
    --log-level=info \
    --log-file=$LOGFILE 2>>$LOGFILE \
    "$@"
