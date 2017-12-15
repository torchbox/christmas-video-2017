FROM python:2.7
LABEL maintainer="Tom Dyson"

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app.py

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
RUN mkdir -p /tmp/videos

COPY . /code/
WORKDIR /code/

EXPOSE 5000
CMD flask run --host=0.0.0.0
