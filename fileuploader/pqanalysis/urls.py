from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.add_attachment, name='add_attachment'),
	url(r'results', views.view_results, name='view_results')
]