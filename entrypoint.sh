#!/bin/sh

# Start ssh daemon
if [ -z ${SSHD_LOG_PATH} ]; then
    SSHD_LOG_PATH=/home/tunnel/sshd.log
fi
/usr/sbin/sshd -f /etc/ssh/sshd_config -E ${SSHD_LOG_PATH}

# Check for secret key
if [[ -z $TUNNEL_SECRET_KEY ]]; then
    export TUNNEL_SECRET_KEY=$(uuidgen)
fi

# Database setup / wait for database
if [ "$SQL_ENGINE" == "postgres" ]; then
    echo "Waiting for postgres..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
elif [[ -z ${SQL_DATABASE} ]]; then
    su tunnel -c "/usr/local/bin/python3 /home/tunnel/web/manage.py makemigrations"
    su tunnel -c "/usr/local/bin/python3 /home/tunnel/web/manage.py migrate"
    su tunnel -c "echo \"import uuid; from django.contrib.auth.models import User; tunnelpass=uuid.uuid4().hex; User.objects.create_superuser('admin', 'admin@example.com', tunnelpass); print(f'admin secret: {tunnelpass}')\" | python manage.py shell"
fi

if [[ ! -d /home/tunnel/web/static ]]; then
    su tunnel -c "/usr/local/bin/python3 /home/tunnel/web/manage.py collectstatic"
fi

if [[ -z $WORKER ]]; then
        echo "Use 1 worker (default)"
        WORKER=1
fi

# Requirement for psycopg2, even if it's not marked by psycopg2 as requirement
# export LD_PRELOAD=/lib/libssl.so.1.1

if [ -z ${UWSGI_PATH} ]; then
    UWSGI_PATH=/home/tunnel/web/uwsgi.ini
fi

su tunnel -c "uwsgi --ini ${UWSGI_PATH} --processes ${WORKER}"
