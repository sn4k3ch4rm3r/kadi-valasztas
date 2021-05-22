from django.http.response import HttpResponse, HttpResponseBadRequest
import requests
from django.shortcuts import redirect, render
from django.views.generic import View
from django.conf import settings

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
		authorized = request.session['email'].endswith('@tanulo.boronkay.hu')
		return render(request, 'voting/vote.html', context={'authorized': authorized})
