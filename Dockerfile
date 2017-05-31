FROM python:2.7
ENV PYTHONUNBUFFERED 1

# install pre-reqs
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
 && rm -rf /var/lib/apt/lists/*

# Setup app
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install gunicorn
ADD . /code/

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/sites-available/campanalogia.conf
RUN ln -s \
    /etc/nginx/sites-available/campanalogia.conf \
    /etc/nginx/sites-enabled/campanalogia.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
