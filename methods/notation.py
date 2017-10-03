#!/usr/bin/env python
# encoding: utf-8
import logging


def sanitise_cccbr_notation(raw_notation):
    """
    Clean up CCCBR notation for JS plotter
        - provide method, return updated method (unsaved)
    """

    lead_head, _raw_notation = _lead_head(raw_notation)

    n_t, notation = [], []
    n_t_reset = False

    # there are edge case problems for Orignal N and Cheeky Little Place Minimus
    if len(_raw_notation) == 1:
        return _edge_cases(_raw_notation), lead_head

    for place in _raw_notation:
        if n_t_reset:
            n_t = []

        if place == '-' or place == '.':
            if n_t:
                notation.append(''.join(n_t))
                n_t = []
            if place == '-':
                notation.append('X')
            n_t_reset = True

        elif place in raw_notation:
            n_t.append(place)
            n_t_reset = False

        else:
            notation.append(''.join(n_t))
            n_t_reset = True

    if n_t:
        notation.append(''.join(n_t))

    return '%s' % notation.__repr__(), lead_head


def _edge_cases(_raw_notation):

    # if we're dealing with original
    if _raw_notation[0] == '-':
        return ['X', '1']

    # if we're dealing with original odd
    elif _raw_notation[0] in ['3', '5', '7', '9', 'E', 'A', 'C']:
        return ['X', '1']

    # if we're dealing with Cheeky Little Place
    elif _raw_notation[0] == '1':
        return ['14', '12']

    else:
        raise Exception('Unknown edge case')


def _lead_head(raw_notation):

    # check for lead head
    if raw_notation.count(',') == 1:
        rns = raw_notation.split(',')

        # we've got a symmetric method
        if len(rns[0]) > len(rns[-1]):
            notation, lead_head = rns

        # we've got a screwy odd bell method
        elif len(rns[0]) < len(rns[-1]):
            lead_head, notation = rns

        else:
            logging.error('unrecognised comma location in {}'.format(raw_notation))
            raise Exception

    elif raw_notation.count(',') == 0:
        notation, lead_head = raw_notation, ''

    else:
        logging.error('more than one "," in {}'.format(raw_notation))
        raise Exception

    return lead_head, notation
