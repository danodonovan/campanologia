import os
from .default import *

DEBUG = True if os.getenv('DEBUG', None) is not None else DEBUG
