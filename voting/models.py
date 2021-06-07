from os import truncate
from django.db import models
from django.utils.timezone import localtime

class KadiCandidate(models.Model):
	name = models.CharField(max_length=40, verbose_name='Név')
	classname = models.CharField(max_length=1, primary_key=True, verbose_name='Osztály')
	color = models.CharField(max_length=20, verbose_name='Szín')

	def __str__(self):
		return self.name + ' - 11. ' + self.classname

	class Meta:
		verbose_name = "Kádi jelölt"
		verbose_name_plural = "Kádi jelöltek"
		

class Vote(models.Model):
	candidate = models.ForeignKey(
		KadiCandidate,
		on_delete=models.DO_NOTHING,
		verbose_name='Jelölt'
	)
	timestamp = models.DateTimeField(verbose_name='Szavazat Ideje', auto_now_add=True)

	def __str__(self):
		print(self.timestamp.astimezone())
		return f'{localtime(self.timestamp).strftime("%Y. %m. %d. %H:%M:%S")} | {self.candidate}'

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

class Period(models.Model):
	start = models.DateTimeField(verbose_name="Kezdés időpontja")
	end = models.DateTimeField(verbose_name="Befejezés időpontja")

	def __str__(self):
		return localtime(self.start).strftime("%Y. %m. %d. %H:%M") + " - " + localtime(self.end).strftime("%Y. %m. %d. %H:%M")
	
	class Meta:
		verbose_name = "Időszak"
		verbose_name_plural = "Időszak"
