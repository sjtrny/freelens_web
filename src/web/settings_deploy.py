import os

from web.settings import *

SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(" ")
CSRF_TRUSTED_ORIGINS = os.environ["CSRF_TRUSTED_ORIGINS"].split(" ")

WSGI_APPLICATION = "web.wsgi.application"
