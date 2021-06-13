from functools import wraps
from voting.models import Period, Voter
from django.http.response import HttpResponseForbidden, HttpResponseServerError
from datetime import datetime
import pytz

from django.shortcuts import redirect, render

def voting_permission_required(function):
	@wraps(function)
	def wrapper(request, *args, **kwargs):
		if 'voter' in request.session:
			user = request.session['voter']
			has_voted = len(Voter.objects.filter(pk=user['mail'])) > 0
			if user['has_voted'] != has_voted:
				request.session['voter']['has_voted'] = has_voted
				request.session.modified = True

			if user['authorized'] and not has_voted:
				return function(request, *args, **kwargs)
			else:
				return HttpResponseForbidden()
		else: 
			return redirect('landing')
	
	return wrapper

def voting_time_period_required(function):
	@wraps(function)
	def wrapper(request, *args, **kwargs):
		period = Period.objects.all()

		if len(period) != 1:
			return HttpResponseServerError()
		
		period = period[0];
		now = datetime.utcnow().replace(tzinfo=pytz.utc)

		if period.start >= now:
			return render(request, 'voting/notstarted.html', context={
				'start': int(datetime.timestamp(period.start))
			})
		
		if period.end <= now:
			return render(request, 'voting/ended.html')

		return function(request, *args, **kwargs)
	
	return wrapper