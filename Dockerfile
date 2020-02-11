FROM python:3.7
ENV PYTHONUNBUFFERED 1

LABEL maintainer="khakshour.amir@gmail.com" \
    com.example.version="0.0.1-alpha"  \
    com.example.release-date="2020-02-11"

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

RUN groupadd -r django && useradd -r -g django django
COPY . /app
RUN chown -R django /app

WORKDIR /app

RUN make install

USER django

RUN make src_build

WORKDIR /app/src/
CMD uwsgi --ini uwsgi.ini

