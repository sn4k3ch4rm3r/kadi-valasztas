from os import truncate
from django.db import models

class KadiCandidate(models.Model):
	firstname = models.CharField(max_length=10)
	lastname = models.CharField(max_length=40)
	nickname = models.CharField(max_length=20, blank=True)
	classname = models.CharField(max_length=1)
	imageurl = models.CharField(max_length=20)

	def __str__(self):
		return self.lastname + ' ' + self.firstname + ' - 11. ' + self.classname
