FROM python:latest

MAINTAINER "sam850118sam@gmail.com"

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir -p /app/tmp

EXPOSE 3000

CMD ["python", "app.py"]