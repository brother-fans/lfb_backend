# !/bin/sh

if [ "$ONLINE_ENV" == "test" ]; then
    echo "========= TEST ========="
    export DJANGO_SETTING_MODULE=config.settings.test
    mkdir /run/daphne
    python manage.py collectstatic
    service cron start
    service cron status
    service nginx start
    supervisord -c /etc/supervisor/supervisord.conf -n
elif [ "$ONLINE_ENV" == "prod" ]; then
    echo "========= PROD ========="
    export DJANGO_SETTING_MODULE=config.settings.prod
    mkdir /run/daphne
    python manage.py collectstatic
    service cron start
    service cron status
    service nginx start
    supervisord -c /etc/supervisor/supervisord.conf -n
else
    echo "ELSE"
    export DJANGO_SETTING_MODULE=config.settings.dev
    service nginx start
    daphne -b 0.0.0.0 -p 8000 --proxy-headers config.asgi:application
fi
