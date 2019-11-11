from django.urls import path
from . import views

urlpatterns = [
	path('app/<str:pk>/', views.AppDetail.as_view()),
	path('cusers/', views.CUserList.as_view()),
	path('cusers/<str:pk>/', views.CUserDetail.as_view()),
	path('searchs/', views.SearchList.as_view()),
	path('books/', views.BookList.as_view()),
]