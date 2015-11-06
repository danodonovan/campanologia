#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import socket

from .settings import *

# get local files
if socket.gethostname().lower() in ('odonovan-pc', 'probeast.local', 'probeast.home'):
    from .host_odonovanpc import *

if socket.gethostname().lower() == 'dodPersonal2':
    from .host_dodPersonal2 import *
