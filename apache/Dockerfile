FROM ubuntu:18.04

# Обновление системы:
RUN apt-get update && apt-get upgrade -y 

# Установка необходимого ПО:
RUN apt-get install -y git apache2 apache2-utils libapache2-mod-wsgi-py3 python3 python3-pip python3-venv
RUN ln /usr/bin/python3 /usr/bin/python && ln /usr/bin/pip3 /usr/bin/pip
RUN apt-get autoremove

#  Настройка виртуальной среды:
RUN mkdir /var/www/html/django_project
ENV VIRTUAL_ENV=/var/www/html/django_project/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONIOENCODING="UTF-8"

# Установка необходимых модулей для django:
WORKDIR /var/www/html/django_project
COPY requirements /var/www/html/django_project/requirements
RUN . venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements 

# Конфигурация git:
ARG git_user_name='dyk_user'
ARG git_user_email='example@email.com'
RUN git config --global user.email $git_user_email \
    && git config --global user.name $git_user_name

# Загрузка кода сайта из github-репозитория:
#RUN git clone --single-branch -b apache https://github.com/TigenTigen/do_you_know.git
# result_path: /var/www/html/django_project/do_you_know/django/config/wsgi.py

# Создание и конфигурация папок для загружаемых и статических файлов:
RUN groupadd media_share && adduser www-data media_share
RUN mkdir /var/www/static/ && chgrp -R media_share /var/www/static/ && chmod -R 776 /var/www/static/

#RUN mkdir /var/www/media/ && mkdir /var/www/html/django_project/do_you_know/django/static/
#RUN chgrp -R media_share /var/www/media/ && chmod -R 776 /var/www/media/
#RUN chgrp -R media_share /var/www/html/django_project/do_you_know/django/static/ \
#    && chmod -R 776 /var/www/html/django_project/do_you_know/django/static/

ADD django-site.conf /etc/apache2/sites-available/000-default.conf

RUN mkdir django

COPY entrypoint_script.sh /var/www/html/django_project/entrypoint_script.sh
ENTRYPOINT . /var/www/html/django_project/entrypoint_script.sh

CMD ["apache2ctl", "-D", "FOREGROUND"]

