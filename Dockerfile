FROM ubuntu:17.10
LABEL maintainer="Tom Dyson"

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    WEB_CONCURRENCY=2 \
    PORT=5000

EXPOSE 5000

WORKDIR /app/

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip ffmpeg x264 libx264-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install uWSGI==2.0.15

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN useradd beatbox
RUN chown -R beatbox .
USER beatbox

COPY . .

CMD ./run.sh
