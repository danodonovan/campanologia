#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from optparse import make_option

from django.core.management.base import BaseCommand

from methods.models import Method, FirstHandbellPeal, FirstTowerbellPeal # MethodSet,
from methods.method_library.db_generator import build_method_db, check_db


class Command(BaseCommand):
    args = '<path to CCCBR xml file> -v=<verbosity>'
    help = 'Populates the methods table from the CCCBR method XML'

    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    option_list = BaseCommand.option_list + (
        make_option('--populate-verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='Verbose DB populate output'),
        )

    def handle(self, file, *args, **options):

        if not os.path.isfile(file):
            raise IOError('file %s not found' % file)

        if options['verbose']:
            self.logger.setLevel(logging.INFO)

        self.populate_db_from_file(file)

    def populate_db_from_file(self, file):

        self.logger.info('populating from file "%s"' % file)

        method_dicts, method_set_dicts = build_method_db(file, logger=self.logger)

        check_db(method_dicts, method_set_dicts)

        self.logger.info('db integrity checks passed')

        for method_set_dict in method_set_dicts:

            # # create the MethodSet object first
            # ms, _ = MethodSet.objects.get_or_create(
            #     id=method_set_dict['methodset_id'],
            #     notes=method_set_dict['notes'],
            #     p_stage=method_set_dict['p_stage'],
            #     p_lengthOfLead=method_set_dict['p_lengthOfLead'],
            #     p_numberOfHunts=method_set_dict['p_numberOfHunts'],
            #     p_huntBellPath=method_set_dict['p_huntBellPath'],
            #     p_symmetry=method_set_dict['p_symmetry'],
            # )
            # self.logger.debug(u'MethodSet %s saved' % ms)
            #
            # assert ms.id == method_set_dict['methodset_id']

            # for method_dict in (item for item in method_dicts if item["methodset_id"] == ms.id):
            #for method_dict in (item for item in method_dicts if item["nbells"] == method_set_dict['p_stage']):
            for method_dict in method_set_dict['methods']:

                # if model exists skip
                if not Method.objects.filter(id=method_dict['id']).exists():

                    # create method linking back to method set
                    m, _ = Method.objects.get_or_create(
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
                    )

                    self.logger.debug(u'Method {nbells} {method} saved'.format(
                        nbells=m.ms_p_stage, method=m.title.decode("utf8"))
                    )

                else:

                    m = Method.objects.get(id=method_dict['id'])

                # first peals
                for peal_tag, peal_obj in (('first_hb_peal', FirstHandbellPeal),
                                           ('first_tb_peal', FirstTowerbellPeal)):

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

                # literature references
                m.rw_reference = method_dict.get('rw_reference', '')
                m.bn_reference = method_dict.get('bn_reference', '')
                m.cb_reference = method_dict.get('cb_reference', '')
                m.pmm_reference = method_dict.get('pmm_reference', '')
                m.tdmm_reference = method_dict.get('tdmm_reference', '')

                # performances = method_dict['performances']
                # references = method_dict['references']
                # falseness = method_dict['falseness']

                # if falseness is not None:
                #     for fs in falseness:
                #         method_dict['falseness_groups'] = find_tag_text(fs, 'fchGroups')
                #         m.falseness_groups = find_tag_text(fs, 'fchGroups')
                #     m.save()

                m.save()

