#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from optparse import make_option

from django.core.management.base import BaseCommand

from methods.models import Method, FirstHandbellPeal, FirstTowerbellPeal
from methods.mongo_models import MongoMethod, MongoFirstHandbellPeal, MongoFirstTowerbellPeal

from methods.method_library.db_generator import build_method_db, check_db


class Command(BaseCommand):
    args = '<path to CCCBR xml file> -v=<verbosity>'
    help = 'Populates the methods table from the CCCBR method XML'

    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    #parser = argparse.ArgumentParser(description=help)

    option_list = BaseCommand.option_list + (
        make_option('--populate-verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='Verbose DB populate output'),
        make_option('--mongodb',
            action='store_true',
            dest='verbose',
            default=False,
            help='Populate MongoDB'),
        )

    def handle(self, file, *args, **options):

        if not os.path.isfile(file):
            raise IOError('file %s not found' % file)

        if options['verbose']:
            self.logger.setLevel(logging.INFO)

        # print options
        # self.use_mongo = options['mongodb']
        self.use_mongo = False

        if self.use_mongo:
            self.Method = MongoMethod
            self.FirstTowerbellPeal = MongoFirstTowerbellPeal
            self.FirstHandbellPeal = MongoFirstHandbellPeal
        else:
            self.Method = Method
            self.FirstTowerbellPeal = FirstTowerbellPeal
            self.FirstHandbellPeal = FirstHandbellPeal

        self.populate_db_from_file(file)

    def populate_db_from_file(self, file):

        self.logger.info('populating from file "%s"' % file)

        method_dicts, method_set_dicts = build_method_db(file, logger=self.logger)

        check_db(method_dicts, method_set_dicts)

        self.logger.info('db integrity checks passed')

        for method_set_dict in method_set_dicts:

            for method_dict in method_set_dict['methods']:

                # if model exists skip
                if not self.Method.objects.filter(id=method_dict['id']).exists():
                # if len(self.Method.objects.filter(id=method_dict['id'])) == 0:

                    # create method linking back to method set
                    m, _ = self.Method.objects.get_or_create(
                        id=method_dict['id'],
                        name=method_dict['name'],
                        classification=method_dict['classification'],
                        raw_notation=method_dict['raw_notation'],
                        title=method_dict['title'],
                        leadHeadCode=method_dict['leadHeadCode'],
                        method_notes=method_dict['method_notes'],
                        # method_set=ms,
                        ms_notes=method_set_dict['notes'],
                        ms_p_stage=method_set_dict['p_stage'],
                        ms_p_lengthOfLead=method_set_dict['p_lengthOfLead'],
                        ms_p_numberOfHunts=method_set_dict['p_numberOfHunts'],
                        ms_p_huntBellPath=method_set_dict['p_huntBellPath'],
                        ms_p_symmetry=method_set_dict['p_symmetry'],
                        # literature references
                        rw_reference=method_dict.get('rw_reference', ''),
                        bn_reference=method_dict.get('bn_reference', ''),
                        cb_reference=method_dict.get('cb_reference', ''),
                        pmm_reference=method_dict.get('pmm_reference', ''),
                        tdmm_reference=method_dict.get('tdmm_reference', ''),
                        # falseness
                        falseness_groups=method_dict.get('falseness_groups', ''),
                    )

                    try:
                        self.logger.debug(u'Method {nbells} {method} saved'.format(
                            nbells=m.ms_p_stage, method=m.title.decode("utf8"))
                        )
                    except UnicodeEncodeError:
                        pass

                else:

                    m = self.Method.objects.get(id=method_dict['id'])

                    try:
                        self.logger.debug(u'Method {nbells} {method} retrieved'.format(
                            nbells=m.ms_p_stage, method=m.title.decode("utf8"))
                        )
                    except UnicodeEncodeError:
                        pass

                # first peals
                for peal_tag, peal_obj in (('first_hb_peal', self.FirstHandbellPeal),
                                           ('first_tb_peal', self.FirstTowerbellPeal)):

                    if peal_tag in method_dict:

                        perf_dict = method_dict[peal_tag]

                        performance, _ = peal_obj.objects.get_or_create(
                            date=perf_dict.get('date', None),
                            building=perf_dict.get('building', None),
                            town=perf_dict.get('town', None),
                            county=perf_dict.get('county', None),
                            region=perf_dict.get('region', None),
                            country=perf_dict.get('country', None),
                            address=perf_dict.get('address', None),
                            location=perf_dict.get('location', None),
                        )

                        setattr(m, peal_tag, performance)

                m.save()

