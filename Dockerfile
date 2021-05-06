# syntax=docker/dockerfile:1
FROM python:3.7
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r requirements.txt
COPY . /code/