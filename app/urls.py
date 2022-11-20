from django.urls import path,re_path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('entry/', views.entry, name='entry'),
	path('group/' , views.group, name='group'),
	re_path('^callback', csrf_exempt(views.callback))
]