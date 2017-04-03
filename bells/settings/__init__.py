from .default import *

DEBUG = True if os.getenv('DEBUG', None) is not None else DEBUG
SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY)
