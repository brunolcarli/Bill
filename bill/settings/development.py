"""
Configs par arodar no Repl.it
"""
from bill.settings.common import *
from decouple import config

SECRET_KEY = config('DJANGO_SECRET_KEY')
