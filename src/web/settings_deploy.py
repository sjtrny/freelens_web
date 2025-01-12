import os

from web.settings import *

SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(" ")

WSGI_APPLICATION = "web.wsgi.application"
