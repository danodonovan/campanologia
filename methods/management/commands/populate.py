#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging

from django.core.management.base import BaseCommand

from methods.models import MethodSet, Method, FirstHandbellPeal, FirstTowerbellPeal

try:
    from lxml import etree
except ImportError:
    print 'installing lxml will speed this up'
    import xml.etree.ElementTree as etree

schema = "http://www.cccbr.org.uk/methods/schemas/2007/05/methods"

def xmlns(tag):
    return "{%s}%s" % (schema, tag)

def find_tag_text(element, tag):
    text = getattr(element.find(xmlns(tag)), 'text', None)
    return str(text.encode("utf-8")) if text else ''

class Command(BaseCommand):
    args = '<path to CCCBR xml file>'
    help = 'Populates the methods table from the CCCBR method XML'

    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def handle(self, file, *args, **options):

        if not os.path.isfile(file):
            raise IOError('file %s not found' % file)

        self.logger.debug('populating from file "%s"' % file)

        tree = etree.parse(file)
        root = tree.getroot()

        for methodSet in root.findall(xmlns('methodSet')):

            properties = methodSet.find(xmlns('properties'))

            # create the MethodSet object first
            ms, _ = MethodSet.objects.get_or_create(
                notes=find_tag_text(methodSet, 'notes'),
                p_stage=find_tag_text(properties, 'stage'),
                p_lengthOfLead=find_tag_text(properties, 'lengthOfLead'),
                p_numberOfHunts=find_tag_text(properties, 'numberOfHunts'),
                p_huntBellPath=find_tag_text(properties, 'huntbellPath'),
                p_symmetry=find_tag_text(properties, 'symmetry'))
            ms.save()

            self.logger.debug(u'MethodSet %s saved' % ms)

            # pull out all the methods in this set
            methods = methodSet.findall(xmlns('method'))

            for method in methods:

                # create method linking back to method set
                m = Method(id=int(method.attrib['id'].split('id')[-1]),
                           method_set=ms,
                           name=find_tag_text(method, 'name'),
                           classification=find_tag_text(method, 'classification'),
                           raw_notation=find_tag_text(method, 'notation'),
                           title=find_tag_text(method, 'title'),
                           leadHeadCode=find_tag_text(method, 'leadHead'),
                           method_notes=find_tag_text(method, 'notes'))

                m.save()

                try: # can't be bothered to fix for Sméagol
                    self.logger.debug(u'Method {method} saved'.format(method=m.title))
                except UnicodeEncodeError:
                    print 'Unicode{De,En}codeError - probably "Sméagol"'
                    pass
                except UnicodeDecodeError:
                    print 'Unicode{De,En}codeError - probably "Sméagol"'
                    pass

                performances = method.find(xmlns('performances'))
                references = method.find(xmlns('references'))
                falseness = method.findall(xmlns('falseness'))

                # create performance (if any) and update method
                if performances is not None:
                    fhbp = performances.find(xmlns('firstHandbellPeal'))
                    ftbp = performances.find(xmlns('firstTowerbellPeal'))

                    if fhbp is not None:

                        perf = FirstHandbellPeal(
                            building=find_tag_text(fhbp, 'building'),
                            town=find_tag_text(fhbp, 'town'),
                            county=find_tag_text(fhbp, 'county'),
                            region=find_tag_text(fhbp, 'region'),
                            country=find_tag_text(fhbp, 'country'),
                            location=find_tag_text(fhbp, 'location'),
                            address=find_tag_text(fhbp, 'address'),
                            date=find_tag_text(fhbp, 'date'))

                        perf.save()
                        m.first_hb_peal = perf
                        m.save()

                        self.logger.debug(u'Handbell Performance %s saved' % perf)

                    if ftbp is not None:
                        perf = FirstTowerbellPeal(
                            building=find_tag_text(ftbp, 'building'),
                            town=find_tag_text(ftbp, 'town'),
                            county=find_tag_text(ftbp, 'county'),
                            region=find_tag_text(ftbp, 'region'),
                            country=find_tag_text(ftbp, 'country'),
                            location=find_tag_text(ftbp, 'location'),
                            address=find_tag_text(ftbp, 'address'),
                            date=find_tag_text(ftbp, 'date'))

                        perf.save()
                        m.first_tb_peal = perf
                        m.save()

                        self.logger.debug(u'Towerbell Performance %s saved' % perf)

                if references is not None:

                    for reference in references:

                        m.rw_reference = find_tag_text(reference, 'rwRef')
                        m.bn_reference = find_tag_text(reference, 'bnRef')
                        m.cb_reference = find_tag_text(reference, 'cbRef')
                        m.pmm_reference = find_tag_text(reference, 'pmmRef')
                        m.tdmm_reference = find_tag_text(reference, 'tdmmRef')

                    m.save()

                if falseness is not None:
                    for fs in falseness:
                        m.falseness_groups = find_tag_text(fs, 'fchGroups')
                    m.save()