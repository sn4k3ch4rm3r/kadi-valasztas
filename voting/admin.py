from django.contrib import admin
from .models import KadiCandidate, Vote, Voter

admin.site.register(KadiCandidate)
admin.site.register(Vote)
admin.site.register(Voter)
