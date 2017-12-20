FROM ubuntu:17.10
LABEL maintainer="Tom Dyson"

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip ffmpeg x264 libx264-dev

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1

COPY ./requirements.txt /code/requirements.txt
RUN pip3 install -r /code/requirements.txt

COPY . /code/
WORKDIR /code/

EXPOSE 5000
CMD ["uwsgi", "--ini", "uwsgi.ini"]
