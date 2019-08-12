from django.urls import path
from . import views

urlpatterns = [
	path('cusers/', views.CUserList.as_view()),
	path('cusers/<int:pk>/', views.CUserDetail.as_view()),
	path('app/', views.AppList.as_view()),
	path('app/<int:pk>', views.AppDetail.as_view()),
	path('searchs/', views.SearchList.as_view()),
	path('searchs/<int:pk>', views.SearchDetail.as_view()),
]