#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import socket

from .settings import *

# get local files
if socket.gethostname() in ('odonovan-pc', 'probeast.home'):
    from .host_odonovanpc import *

if socket.gethostname() == 'dodPersonal2':
    from .host_dodPersonal2 import *
