FROM ubuntu:16.04
LABEL maintainer="Tom Dyson"

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip ffmpeg x264 libx264-dev

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=xmasvideo/app.py

COPY ./requirements.txt /code/requirements.txt
RUN pip3 install -r /code/requirements.txt

COPY . /code/
WORKDIR /code/

EXPOSE 5000
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
