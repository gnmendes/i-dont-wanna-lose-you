FROM python:3.9-slim

RUN apt-get update \
    && apt-get install ffmpeg -y

ADD . /idontwannaloseyou
WORKDIR /idontwannaloseyou
RUN pip3 install -r requirements.txt
ENV FLASK_APP=idontwannaloseyou/controller/
