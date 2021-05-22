from .base import *
import django_heroku

DEBUG = False

ALLOWED_HOSTS = ['kadi-vote.herokuapp.com']

django_heroku.settings(locals())