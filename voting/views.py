from django.http.response import HttpResponseBadRequest
from django.urls import reverse
import requests
from django.shortcuts import redirect, render
from django.views.generic import View
from django.conf import settings
from .models import KadiCandidate
import random 

class LandingPage(View):
	def get(self, request):
		oa_url = settings.OA_URL_TEMPLATE.format(
			client_id = settings.OA_CLIENT_ID,
			redirect = settings.OA_REDIRECT,
			scope = ' '.join(settings.OA_SCOPE),
			state = 1,
		)
		return render(request, 'voting/landing.html', context={'oauthlink': oa_url})

class Authenticate(View):
	def get(self, request):
		if 'code' in request.GET:
			code = request.GET['code']
			resp = requests.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', 
				data= {
					"grant_type": "authorization_code",
					"client_id": settings.OA_CLIENT_ID,
					"client_secret": settings.OA_CLIENT_SECRET,
					"scope": ' '.join(settings.OA_SCOPE),
					"redirect_uri": settings.OA_REDIRECT,
					"code": code,
				}
			)
			try:
				token = resp.json()['access_token']

				resp = requests.get('https://graph.microsoft.com/v1.0/me/', headers={'Authorization':f'Bearer {token}'})
				request.session['email'] = resp.json()['userPrincipalName']
				request.session['access_token'] = token
				return redirect('vote')
			except:
				return HttpResponseBadRequest()

class Vote(View):
	def get(self, request):
		candidates = KadiCandidate.objects.all()
		candidates = random.sample(list(candidates), len(candidates))
		authorized = request.session['email'].endswith('@tanulo.boronkay.hu')

		return render(request, 'voting/vote.html', 
		context= {
				'authorized': authorized,
				'candidates': candidates,
			}
		)

def logout(request):
	request.session.clear()
	return redirect(f"https://login.microsoftonline.com/common/oauth2/v2.0/logout?post_logout_redirect_uri={get_current_host(request) + reverse('landing')}")

def get_current_host(request) -> str:
    scheme = request.is_secure() and "https" or "http"
    return f'{scheme}://{request.get_host()}'