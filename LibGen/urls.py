from django.urls import path
from . import views

urlpatterns = [
	path('copy/', views.CopyUser.as_view())
]