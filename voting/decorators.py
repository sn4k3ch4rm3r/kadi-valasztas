from functools import wraps
from django.http.response import HttpResponseForbidden

from django.shortcuts import redirect, render

def voting_permission_required(function):
	@wraps(function)
	def wrapper(request, *args, **kwargs):
		if 'user' in request.session:
			user = request.session['user']

			if user['authorized']:
				return function(request, *args, **kwargs)
			else:
				return HttpResponseForbidden()
		else: 
			return redirect('landing')
	
	return wrapper