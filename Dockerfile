FROM ubuntu:14

ENV TZ "Asia/Shanghai"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ARG ONLINE_ENV
ENV ONLINE_ENV=$ONLINE_ENV

COPY ./sources.list /etc/apt

RUN apt-get update \
    && apt-get install -y nginx supervisor net-tools dsniff lsof \
    && apt-get install -y libsasl2-dev libldap2-dev vim cron less procps

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./supervisor.conf /etc/supervisor/supervisord.conf
COPY ./lfb_backend /srv/
WORKDIR /srv

RUN pip3 install --upgrade --no-cache-dir pip
RUN pip3 install --no-cache-dir incremental
RUN pip3 install --no-cache-dir twisted
RUN pip3 install --no-cache-dir -I boto3==1.9.148
RUN pip3 install --no-cache-dir \
    django \
    uwsgi \
    requests \
    djangorestframework \
    django-queryset-csv \
    xpinyin \
    pandas \
    numpy \
    gensim \
    xlrd \
    xlwt \
    silk \
    emoji \
    python-dateutil \
    elasticsearch \
    redis \
    mysqlclient \
    django-bulk-update \
    any_case

RUN ["chmod", "+X" "/srv/start_script.sh"]

EXPOSE 80
CMD ["bash", "srv/start_script.sh"]
