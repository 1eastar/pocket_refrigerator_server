FROM        python:3.8.1-slim
MAINTAINER  ehdwls6703@gmail.com

RUN         apt -y update && apt -y dist-upgrade
RUN         apt -y install build-essential
RUN         apt -y install nginx supervisor
RUN         apt -y install libpcre3 libpcre3-dev python-dev

# WORKDIR     /srv
# RUN         python -m venv myvenv
# RUN         . myvenv/bin/activate
# RUN         export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python3.8"
# RUN         export PYTHONPATH="${PYTHONPATH}:/srv/djangobackend/myvenv/lib/python3.8/site-packages"

ENV         PROJECT_DIR              /srv/pocketrefriserver

COPY        .                       ${PROJECT_DIR}
WORKDIR     /srv/pocketrefriserver
RUN         pip install -r requirements.txt
RUN         python manage.py makemigrations
RUN         python manage.py migrate
RUN         echo "from common.models import User; User.objects.filter(nickname='happyhappy1').delete(); User.objects.create_superuser('ehdwls6703@gmail.com', 'happyhappy1', 'happyhappy1')" | python manage.py shell
WORKDIR     ${PROJECT_DIR}

RUN         cp -f ${PROJECT_DIR}/.config/nginx.conf           /etc/nginx
RUN         cp -f ${PROJECT_DIR}/.config/pocketrefriserver      /etc/nginx/sites-available

RUN         rm -f /etc/nginx/sites-enabled/*
RUN         ln -fs /etc/nginx/sites-available/pocketrefriserver                  /etc/nginx/sites-enabled

RUN         cp -f ${PROJECT_DIR}/.config/supervisor_app.conf  /etc/supervisor/conf.d

EXPOSE      80

CMD         supervisord -n