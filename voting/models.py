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

	class Meta:
		verbose_name = "Kádi jelölt"
		verbose_name_plural = "Kádi jelöltek"
		

class Vote(models.Model):
	candidate = models.ForeignKey(KadiCandidate, on_delete=models.DO_NOTHING)

	def __str__(self):
		return str(self.candidate)

	class Meta:
		verbose_name = "Szavazat"
		verbose_name_plural = "Szavazatok"

class Voter(models.Model):
	email = models.CharField(max_length=100, primary_key=True)
	refresh_token = models.TextField()

	def __str__(self):
		return self.email

	class Meta:
		verbose_name = "Szavazó"
		verbose_name_plural = "Szavazók"