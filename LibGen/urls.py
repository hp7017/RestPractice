from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from . import models
from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.shortcuts import reverse

info_dict = {
	'queryset': models.Book.objects.all()
}

class StaticSitemap(Sitemap):

	def items(self):
		return ['index', 'profile', 'disclaimer', 'contact_us']

	def location(self, item):
		return reverse(item)

urlpatterns = [
	path('', views.Index.as_view(), name='index'),
	path('profile', views.Profile.as_view(), name='profile'),
	path('disclaimer', views.Disclaimer.as_view(), name='disclaimer'),
	path('search', views.Search.as_view(), name='search'),
	path('evaluations', views.Evaluation.as_view(), name='evaluations'),
	path('books/<str:slug>/<int:pk>', views.BookDetail.as_view(), name='books'),
	path('ads-manager', views.AdsManager.as_view(), name='ads-manager'),
	path('sponsored-book-clicked', views.SponsoredBookClicked.as_view(), name='sponsored_book_clicked'),
	path('recharge-clicked', views.RechargeClicked.as_view(), name='recharge_clicked'),
	path('create-wallet', views.CreateWallet.as_view(), name='create_wallet'),
	path('keyword-planner_clicked/', views.KeywordPlannerClicked.as_view(), name='keyword_planner_clicked'),
	path('sitemap.xml', sitemap, {'sitemaps': {'static': StaticSitemap(), 'books': GenericSitemap(info_dict)}}, name='django.contrib.sitemap.views.sitemap'),
	path('payment-done', views.payment_done, name='payment_done'),
	path('payment-return', views.payment_return, name='payment_return'),
	path('contact-us', views.ContactUs.as_view(), name='contact_us'),
	path('book-clicked', views.BookClicked.as_view(), name='book_clicked'),
	path('oops', views.Oops.as_view(), name='oops'),
	path('our-policy', views.our_policy, name='our_policy'),
	path('terms-condition', views.terms_condition, name='terms_condition'),
	path('about-us', views.about_us, name='about_us'),
]