from functools import wraps
from voting.models import Voter
from django.http.response import HttpResponseForbidden

from django.shortcuts import redirect, render

def voting_permission_required(function):
	@wraps(function)
	def wrapper(request, *args, **kwargs):
		if 'user' in request.session:
			user = request.session['user']
			has_voted = len(Voter.objects.filter(pk=user['mail'])) > 0
			if user['has_voted'] != has_voted:
				request.sesion['user']['has_voted'] = has_voted
				request.session.modified = True

			if user['authorized'] and not has_voted:
				return function(request, *args, **kwargs)
			else:
				return HttpResponseForbidden()
		else: 
			return redirect('landing')
	
	return wrapper
