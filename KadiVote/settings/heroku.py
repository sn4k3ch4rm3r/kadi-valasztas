from .base import *
import django_heroku

DEBUG = os.environ['DEBUG']

ALLOWED_HOSTS = ['kadi-vote.herokuapp.com']

django_heroku.settings(locals())