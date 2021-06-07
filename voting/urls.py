from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
	path('', views.LandingPage.as_view(), name='landing'),
	path('auth/', views.Authenticate.as_view(), name='auth'),
	path('vote/', views.Vote.as_view(), name='vote'),
	path('howitworks/', TemplateView.as_view(template_name='voting/howitworks.html'), name='howitworks'),
	path('logout/', views.logout, name='logout'),
	path('postlogin/', views.PostLogin.as_view(), name='postlogin'),
	path('done/', views.Done.as_view(), name='confirmation'),
	path('results/', views.Results.as_view(), name='results'),
	path('.well-known/microsoft-identity-association.json', views.ms_well_known, name='ms_well-known')
]
