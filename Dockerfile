FROM ubuntu:16.04
LABEL maintainer="Tom Dyson"

RUN apt-get update
RUN apt-get install -y ffmpeg x264 libx264-dev
RUN apt-get install -y python python-pip
RUN apt-get install -y python-opencv

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app.py

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
RUN mkdir -p /tmp/videos

COPY . /code/
WORKDIR /code/

EXPOSE 5000
CMD flask run --host=0.0.0.0
