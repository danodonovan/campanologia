#!/bin/bash

# $Id: $
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py populate --xml-file allmeths.xml

curl 192.168.1.100:8000
