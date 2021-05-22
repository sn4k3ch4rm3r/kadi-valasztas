from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
	path('', views.LandingPage.as_view(), name='landing'),
	path('auth/', views.Authenticate.as_view(), name='auth'),
	path('vote/', views.Vote.as_view(), name='vote'),
	path('howitowrks/', TemplateView.as_view(template_name='voting/howitworks.html'), name='howitworks'),
	path('logout/', views.logout, name='logout'),
]
