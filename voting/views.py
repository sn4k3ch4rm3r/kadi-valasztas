from voting.decorators import voting_permission_required
from django.http.response import HttpResponseBadRequest
from django.urls import reverse
import requests
from django.shortcuts import redirect, render
from django.views.generic import View
from django.conf import settings
from .models import KadiCandidate, Voter, Vote as VoteModel
import random 
from django.utils.decorators import method_decorator

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
				refresh_token = resp.json()['refresh_token']

				resp = requests.get('https://graph.microsoft.com/v1.0/me/', headers={'Authorization':f'Bearer {token}'})
				user = resp.json()

				user['authorized'] = user['userPrincipalName'].endswith('@tanulo.boronkay.hu')
				user['refresh_token'] = refresh_token
				user['has_voted'] = len(Voter.objects.filter(pk=user['mail'])) > 0

				request.session['user'] = user
				return redirect('postlogin')
			except:
				return HttpResponseBadRequest()

@method_decorator(voting_permission_required, name='dispatch')
class Vote(View):
	def get(self, request):
		candidates = KadiCandidate.objects.all()
		candidates = random.sample(list(candidates), len(candidates))

		return render(request, 'voting/vote.html', 
		context= {
				'candidates': candidates,
			}
		)
	def post(self, request):
		voted_class = request.POST['kadi']
		candidate = KadiCandidate.objects.filter(pk=voted_class)
		if len(candidate) == 0:
			return HttpResponseBadRequest()
		candidate = candidate[0]
		
		voter = Voter(email = request.session['user']['userPrincipalName'], refresh_token = request.session['user']['refresh_token'])
		vote = VoteModel(candidate = candidate)
		
		voter.save()
		vote.save()

		return redirect('howitworks')

def logout(request):
	request.session.clear()
	return redirect(f"https://login.microsoftonline.com/common/oauth2/v2.0/logout?post_logout_redirect_uri={get_current_host(request) + reverse('landing')}")

def get_current_host(request) -> str:
    scheme = request.is_secure() and "https" or "http"
    return f'{scheme}://{request.get_host()}'