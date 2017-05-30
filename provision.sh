#!/bin/bash

# $Id: $
# docker-compose up -d
# force 'web' image to be built
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py populate --xml-file allmeths.xml

curl 192.168.1.100:8000
