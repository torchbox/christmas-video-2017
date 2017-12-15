FROM ubuntu:16.04
LABEL maintainer="Tom Dyson"

RUN apt-get update
RUN apt-get install -y ffmpeg x264 libx264-dev
RUN apt-get install -y python3 python3-pip

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP xmasvideo/app.py

COPY ./requirements.txt /code/requirements.txt
RUN pip3 install -r /code/requirements.txt
RUN mkdir -p /tmp/videos

COPY . /code/
WORKDIR /code/

EXPOSE 5000
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
