FROM python:3.7-slim-buster

WORKDIR /usr/src/app


RUN apt update ; apt install -y  \
      ca-certificates   \
      bash              \
      coreutils         \
      gcc               \
      git               \
      make              \
      wget              \
      gnupg             \
      python3-mysqldb ;

RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db
RUN curl -LsS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash
RUN apt install -y apt-transport-https
RUN apt update ; apt upgrade; \
    apt install -y  libmariadb3 libmariadb-dev;


COPY requirements.txt ./
RUN  pip3.7 install --upgrade pip && \
     pip3.7  install --no-cache-dir -r requirements.txt

COPY gunicorn_starter.sh /usr/src/app
COPY *.py /usr/src/app
COPY api /usr/src/app/api
RUN chmod +x /usr/src/app/gunicorn_starter.sh

ENTRYPOINT ["./gunicorn_starter.sh"]
