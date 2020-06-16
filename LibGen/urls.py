from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from . models import Book
from django.contrib.sitemaps import GenericSitemap

info_dict = {
    'queryset': Book.objects.all(),
    'date_field': 'date',
}

urlpatterns = [
	path('', views.Index.as_view(), name='index'),
	path('profile', views.Profile.as_view(), name='profile'),
	path('disclaimer', views.Disclaimer.as_view(), name='disclaimer'),
	path('search', views.Search.as_view(), name='search'),
	path('evaluations', views.Evaluation.as_view(), name='evaluations'),
	path('books/<int:pk>', views.BookDetail.as_view(), name='books'),
	path('sitemap.xml', sitemap, {'sitemaps': {'books': GenericSitemap(info_dict, priority=0.6)}}, name='django.contrib.sitemap.views.sitemap')
]