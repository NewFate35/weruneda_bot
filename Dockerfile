FROM python:3.9-slim-buster as builder

WORKDIR /src
COPY requirements.txt /src
RUN pip install -r requirements.txt
COPY . /src
