from django.urls import path
from . import views

urlpatterns = [
	path('polls/', views.PollList.as_view()),
	path('polls/<int:pk>/', views.PollDetail.as_view()),
	path('polls/choices/', views.ChoiceList.as_view()),
	path('polls/choices/<int:pk>', views.ChoiceDetail.as_view()),
	path('polls/votes/', views.VoteList.as_view()),
	path('polls/votes/<int:pk>', views.VoteDetail.as_view()),
	path('polls/users/', views.UserList.as_view())
]
