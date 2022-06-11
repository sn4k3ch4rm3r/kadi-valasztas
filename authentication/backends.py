from django.contrib.auth.backends import BaseBackend
from .models import User
import requests

class OAuthBackend(BaseBackend):
	def authenticate(self, request, token=None):
		resp = requests.get('https://graph.microsoft.com/v1.0/me/', headers={'Authorization':f'Bearer {token}'})
		data = resp.json()

		user = User.objects.filter(email=data['userPrincipalName'])
		if not user.exists():
			user = User(email=data['userPrincipalName'])
		else:
			user = user[0]

		user.display_name = data['displayName']
		user.save()
		return user