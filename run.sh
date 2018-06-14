#!/bin/sh
set -xe

export UWSGI_HTTP_SOCKET=":$PORT"
export UWSG_WORKERS="$WEB_CONCURRENCY"

exec uwsgi --ini uwsgi.ini
