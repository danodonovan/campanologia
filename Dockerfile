FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install gunicorn
ADD . /code/

EXPOSE 5000
