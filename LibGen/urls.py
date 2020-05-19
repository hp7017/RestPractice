from django.urls import path
from . import views

urlpatterns = [
	path('cuser/<str:user_pk>/searchs/<int:search_pk>/book/', views.CreateBook.as_view()),
	path('cuser/<str:user_pk>/searchs/', views.CreateSearch.as_view()),
	path('cusers/', views.CreateUser.as_view()),

	path('app/<str:pk>/', views.ReadEnvirementVariable.as_view()),
]