from os import truncate
from django.db import models
from django.db.models.fields import CharField

class KadiCandidate(models.Model):
	firstname = models.CharField(max_length=10)
	lastname = models.CharField(max_length=40)
	nickname = models.CharField(max_length=20, blank=True)
	classname = models.CharField(max_length=1, primary_key=True)
	imageurl = models.CharField(max_length=20)

	def __str__(self):
		return self.lastname + ' ' + self.firstname + ' - 11. ' + self.classname

class Vote(models.Model):
	classname = models.ForeignKey(KadiCandidate, on_delete=models.DO_NOTHING)

class Voter(models.Model):
	email = models.CharField(max_length=100, primary_key=True)
	refresh_token = models.TextField()