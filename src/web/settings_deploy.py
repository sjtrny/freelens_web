import os
from pathlib import Path

from web.settings import *

SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# TODO PULL FROM ENVIRONMENT
ALLOWED_HOSTS = []

WSGI_APPLICATION = "web.wsgi.application"
