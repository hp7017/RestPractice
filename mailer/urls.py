from django.urls import path
from mailer import views

urlpatterns = [
	path('', views.Index.as_view(), name='index'),
]

app_name = 'mailer'