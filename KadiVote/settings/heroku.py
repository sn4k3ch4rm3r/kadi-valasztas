from KadiVote.settings.dev import DATABASES
from .base import *
import django_heroku
import dj_database_url

DEBUG = os.environ['DEBUG']

ALLOWED_HOSTS = ['kadi-vote.herokuapp.com']

django_heroku.settings(locals())

DATABASES = {
	'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}