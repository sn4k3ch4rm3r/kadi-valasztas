from django.contrib import admin
from .models import KadiCandidate, Period, Vote
from django.conf import settings
from csvexport.actions import csvexport

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
	list_display = ['timestamp', 'candidate']
	actions = [csvexport]

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
	list_display = ['start', 'end']
	
	def has_add_permission(self, request):
		return Period.objects.count() < 1


admin.site.register(KadiCandidate)
