from django.urls import path
from django.views.generic.base import View

from . import views

urlpatterns = [
	path('', views.LandingPage.as_view(), name='landing'),
	path('auth/', views.Authenticate.as_view(), name='auth'),
	path('vote/', views.Vote.as_view(), name='vote'),
]
