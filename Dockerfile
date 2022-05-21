FROM python:3.10.4-slim-buster

WORKDIR /working_directory

COPY requirements.txt .

RUN apt-get update

RUN pip install --upgrade pip && \
    pip install -r requirements.txt