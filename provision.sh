#!/bin/bash

# $Id: $
# docker-compose up -d
# force 'web' image to be built
docker-compose up --build -d
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py populate --xml-file allmeths.xml
