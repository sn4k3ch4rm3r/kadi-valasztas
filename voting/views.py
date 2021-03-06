from voting.decorators import voting_permission_required, voting_time_period_required
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.urls import reverse
import requests
from django.shortcuts import redirect, render
from django.views.generic import View
from django.conf import settings
from .models import KadiCandidate, Vote as VoteModel
import random 
from django.utils.decorators import method_decorator
from authentication.backends import OAuthBackend
from django.contrib.auth import login, logout

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
				login(request, OAuthBackend.authenticate(self, request, token))
				return redirect('postlogin')
			except:
				return HttpResponseBadRequest()

@method_decorator(voting_time_period_required, name='dispatch')
class PostLogin(View):
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('landing')
		return render(request, 'voting/postlogin.html')

@method_decorator([voting_time_period_required, voting_permission_required], name='dispatch')
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
		
		request.user.has_voted = True
		request.user.save()
		vote = VoteModel(candidate = candidate)
		
		vote.save()

		return redirect('confirmation')

@method_decorator(voting_time_period_required, name='dispatch')
class Done(View):
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('landing')
		elif not request.user.has_voted:
			return redirect('postlogin')
		return render(request, 'voting/confirmation.html')

class Results(View):
	def get(self, request):
		votes = VoteModel.objects.all()
		context = dict()

		if len(votes) > 0:
			summary = dict.fromkeys(KadiCandidate.objects.all(), 0)
			timelines = dict(summary)

			for candidate in timelines.keys():
				timelines[candidate] = dict()
				timelines[candidate]['data'] = list()

			for vote in votes[:len(votes)]:
				summary[vote.candidate] += 1
				timelines[vote.candidate]['data'].append({
					'x': str(vote.timestamp),
					'y': summary[vote.candidate]
				})
			
			summary = dict(sorted(summary.items(), key=lambda item: item[1], reverse=True))

			timelines_context = []
			for tl in timelines.keys():
				tld = {
					'candidate': tl,
					'data': timelines[tl]['data'],
				}
				if len(tld['data']) == 0 or tld['data'][len(tld['data'])-1]['x'] != str(votes[len(votes)-1].timestamp):
					tld['data'].append({
						'x': str(votes[len(votes)-1].timestamp),
						'y': summary[tl],
					})
				timelines_context.append(tld)

			context = {
				'summary': {
					'labels': list(map(str, list(summary.keys()))),
					'data': list(summary.values()),
					'colors': [x.color for x in summary.keys()]
				},
				'timelines': timelines_context
			}
		context['total'] = len(votes)
		return render(request, 'voting/results.html', context=context)

def ms_well_known(request):
	data = {
		"associatedApplications": [
			{
				"applicationId": "5a9a502a-59bb-4e3f-a1a3-e30bf92de601"
			}
		]
	}
	return JsonResponse(data)

def logout_endpoint(request):
	logout(request)
	return redirect(f"https://login.microsoftonline.com/common/oauth2/v2.0/logout?post_logout_redirect_uri={get_current_host(request) + reverse('landing')}")

def get_current_host(request) -> str:
    scheme = request.is_secure() and "https" or "http"
    return f'{scheme}://{request.get_host()}'