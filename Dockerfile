FROM python:3.9-slim

RUN apt-get update \
    && apt-get install ffmpeg -y \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

ADD . /idontwannaloseyou
WORKDIR /idontwannaloseyou
RUN pip3 install -r requirements.txt
ENV FLASK_APP=idontwannaloseyou/content/content_controller.py
