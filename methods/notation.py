#!/usr/bin/env python
# encoding: utf-8
import logging


def sanitise_cccbr_notation(raw_notation):
    """
    Clean up CCCBR notation for JS plotter
        - provide method, return updated method (unsaved)
    """

    # check for lead head
    if raw_notation.count(',') == 1:
        rns = raw_notation.split(',')

        # we've got a symmetric method
        if len(rns[0]) > len(rns[-1]):
            nr, lh = rns

        # we've got a screwy odd bell method
        elif len(rns[0]) < len(rns[-1]):
            lh, nr = rns

    elif raw_notation.count(',') == 0:
        nr, lh = raw_notation, ''

    else:
        logging.error('more than one "," in %s : %s' % raw_notation)
        raise Exception

    i = 0
    n_t, n = [], []
    n_t_reset = False

    # there are edge case problems for Orignal N and Cheeky Little Place Minimus
    if len(nr) == 1:
        # if we're dealing with original
        if nr[0] == '-':
            n.extend(['X', '1'])
            return n, lh

        # if we're dealing with original odd
        if nr[0] in ['3', '5', '7', '9', 'E', 'A', 'C']:
            n.extend(['X', '1'])
            return n, lh

        # if we're dealing with Cheeky Little Place
        elif nr[0] == '1':
            n.extend(['14', '12'])
            return n, lh

    while i < len(nr):
        if n_t_reset:
            n_t = []

        if nr[i] == '-' or nr[i] == '.':
            if n_t:
                n.append(''.join(n_t))
                n_t = []
            if nr[i] == '-':
                n.append('X')
            n_t_reset = True

        elif nr[i] in raw_notation:
            n_t.append(nr[i])
            n_t_reset = False

        else:
            n.append(''.join(n_t))
            n_t_reset = True

        i += 1

    if n_t:
        n.append(''.join(n_t))

    return '%s' % n.__repr__(), lh
