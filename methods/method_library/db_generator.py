import logging

try:
    from lxml import etree
except ImportError:
    print 'installing lxml will speed this up'
    import xml.etree.ElementTree as etree

schema = "http://www.cccbr.org.uk/methods/schemas/2007/05/methods"

def xmlns(tag):
    return "{%s}%s" % (schema, tag)


def find_tag_text(element, tag):
    if element is None: return ''
    text = getattr(element.find(xmlns(tag)), 'text', None)
    return str(text.encode("utf-8")) if text else ''


def create_performance_dict(fhbp):
    location = fhbp.find(xmlns('location'))
    perf_dict = {
        'building': find_tag_text(location, 'building'),
        'town': find_tag_text(location, 'town'),
        'county': find_tag_text(location, 'county'),
        'region': find_tag_text(location, 'region'),
        'country': find_tag_text(location, 'country'),
        'location': find_tag_text(location, 'location'),
        'address': find_tag_text(location, 'address'),
        'date': find_tag_text(fhbp, 'date')
    }
    return perf_dict


def update_method_dict(method_dict, references):
    method_dict['rw_reference'] = find_tag_text(references, 'rwRef')
    method_dict['bn_reference'] = find_tag_text(references, 'bnRef')
    method_dict['cb_reference'] = find_tag_text(references, 'cbRef')
    method_dict['pmm_reference'] = find_tag_text(references, 'pmmRef')
    method_dict['tdmm_reference'] = find_tag_text(references, 'tdmmRef')
    return method_dict


def create_method_set_dict(methodset, methodset_id):
    properties = methodset.find(xmlns('properties'))
    method_set_dict = {
        'methodset_id': methodset_id,
        'notes': find_tag_text(methodset, 'notes'),
        'p_stage': find_tag_text(properties, 'stage'),
        'p_lengthOfLead': find_tag_text(properties, 'lengthOfLead'),
        'p_numberOfHunts': find_tag_text(properties, 'numberOfHunts'),
        'p_huntBellPath': find_tag_text(properties, 'huntbellPath'),
        'p_symmetry': find_tag_text(properties, 'symmetry')
    }
    return method_set_dict


def create_method_dict(method, methodset_id):
    method_dict = {
        'id': int(method.attrib['id'].split('id')[-1]),
        'methodset_id': methodset_id,
        'name': find_tag_text(method, 'name'),
        'classification': find_tag_text(method, 'classification'),
        'raw_notation': find_tag_text(method, 'notation'),
        'title': find_tag_text(method, 'title'),
        'leadHeadCode': find_tag_text(method, 'leadHead'),
        'method_notes': find_tag_text(method, 'notes')
    }
    return method_dict


def build_method_db(file, logger=None, limit=None):

    if logger is not None:
        logger.debug('build_method_db %s' % file)

    tree = etree.parse(file)
    root = tree.getroot()

    method_dicts = []
    method_set_dicts = []

    for ms_id, methodSet in enumerate(root.findall(xmlns('methodSet'))):

        method_set_dict = create_method_set_dict(methodSet, ms_id + 1)

        if logger is not None:
            logger.debug('method set %s' % method_set_dict['p_stage'])

        # pull out all the methods in this set
        methods = methodSet.findall(xmlns('method'))

        for method in methods:

            # create method linking back to method set
            method_dict = create_method_dict(method, ms_id)

            if logger is not None:
                logger.debug('method %s' % method_dict['name'])

            performances = method.find(xmlns('performances'))
            references = method.find(xmlns('references'))
            falseness = method.findall(xmlns('falseness'))

            # create performance (if any) and update method
            if performances is not None:
                fhbp = performances.find(xmlns('firstHandbellPeal'))
                ftbp = performances.find(xmlns('firstTowerbellPeal'))

                if fhbp is not None:

                    perf_dict = create_performance_dict(fhbp)

                    if 'first_hb_peal' not in method_dict:
                        method_dict['first_hb_peal'] = perf_dict

                if ftbp is not None:

                    perf_dict = create_performance_dict(ftbp)

                    if 'first_tb_peal' not in method_dict:
                        method_dict['first_tb_peal'] = perf_dict

            if references is not None:

                method_dict = update_method_dict(method_dict, references)

            if falseness is not None:
                for fs in falseness:
                    method_dict['falseness_groups'] = find_tag_text(fs, 'fchGroups')

            method_dicts.append(method_dict)

        method_set_dicts.append(method_set_dict)

        if limit is not None and method_dict['id'] > limit:
            break

    return method_dicts, method_set_dicts


def check_db(md, msd):

    # assert all ids in method_dicts are unique
    assert all([(i+1) == m['id'] for i, m in enumerate(md)])

    assert all([(i+1) == m['methodset_id'] for i, m in enumerate(msd)])

    print 'assert ok'


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    methods_file = '../../allmeths.xml'

    md, msd = build_method_db(methods_file, logger=logger, limit=20)

    check_db(md, msd)