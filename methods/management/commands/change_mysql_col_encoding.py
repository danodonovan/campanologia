#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

import MySQLdb

class Command(BaseCommand):
    args = '<name of table to change>'
    help = 'change mysql column encoding'

    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def handle(self, *args, **options):

        host = settings.DATABASES['default']['HOST']
        passwd = settings.DATABASES['default']['PASSWORD']
        user = settings.DATABASES['default']['USER']
        dbname = settings.DATABASES['default']['NAME']

        db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
        cursor = db.cursor()

        command = "ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'" % dbname
        self.logger.info("> %s" % command)
        cursor.execute(command)

        sql = "SELECT DISTINCT(table_name) FROM information_schema.columns WHERE table_schema = '%s'" % (dbname)
        self.logger.info("> %s" % sql)
        cursor.execute(sql)

        results = cursor.fetchall()
        for row in results:
            sql = "ALTER TABLE `%s` convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
            self.logger.info(">> %s" % sql)
            cursor.execute(sql)
        db.close()
