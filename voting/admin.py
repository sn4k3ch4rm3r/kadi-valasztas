from django.contrib import admin
from .models import KadiCandidate, Vote, Voter
from django.conf import settings

class ReadOnlyAdmin(admin.ModelAdmin):
	def has_add_permission(self, request):
		if settings.DEBUG:
			return super().has_change_permission(request)
		else:
			return False
	def has_delete_permission(self, request, obj=None):
		if settings.DEBUG:
			return super().has_change_permission(request, obj=obj)
		else:
			return False
	def has_change_permission(self, request, obj=None):
		if settings.DEBUG:
			return super().has_change_permission(request, obj=obj)
		else:
			return False
	actions = None

@admin.register(Vote)
class VoteAdmin(ReadOnlyAdmin):
	readonly_fields = ['candidate']
	

@admin.register(Voter)
class VoterAdmin(ReadOnlyAdmin):
	readonly_fields = ['email', 'refresh_token']

admin.site.register(KadiCandidate)
