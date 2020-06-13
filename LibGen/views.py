from . import models
from django.views import View
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404, reverse
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup
from textblob import Word
from django.db.models import Q

# Create your views here.

class Book():
	title = None
	author = None
	size = None
	extension = None

class SynonymAndDef():
	synonyms = None
	word = None
	definitions = None

class CustomSponsoredBook():
	obj = models.SponsoredBook.objects.none()
	points = 0

	def __repr__(self):
		return f'{self.obj} with {self.points}'

class Index(View):

	def get(self, request):
		user = get_object_or_404(User, id=3)
		intrests = user.intrests.all()
		final_sponsored_books = []
		count = 0
		for intrest in intrests:
			print(intrest)
			sponsored_books = models.SponsoredBook.objects.filter(verified=True, keywords__title__iexact=intrest)
			print(sponsored_books)
			if sponsored_books.exists():
				sponsored_books = list(sponsored_books)
				for sponsored_book in sponsored_books:
					should_continue = False
					for custom_sponsored_book in final_sponsored_books:
						if custom_sponsored_book.obj == sponsored_book:
							custom_sponsored_book.points += 1
							should_continue =True
							break
					if should_continue:
						continue
					custom_sponsored_book = CustomSponsoredBook()
					custom_sponsored_book.obj = sponsored_book
					final_sponsored_books.append(custom_sponsored_book)
			if len(final_sponsored_books) == 6:
				break
		final_sponsored_books.sort(key=lambda x: x.points, reverse=True)
		context = {
			'user': user,
			'sponsored_books': final_sponsored_books
		}
		return render(request, 'index.html', context=context)

class Profile(View):

	def get(self, request):
		user = get_object_or_404(User, id=3)
		context = {
			'user' : user
		}
		return render(request, 'profile.html', context=context)

class Disclaimer(View):

	def get(self, request):
		return render(request, 'disclaimer.html')

class Search(View):

	def parsed(self, search):
		words = []
		having_related_words = False
		having_definitions = False
		keywords = search.split(' ')
		user = User.objects.get(pk=3)
		search_model = models.Search.objects.create(search=search, user=user)
		search_model.save()
		for keyword in keywords:
			if len(keyword) == 1 or keyword.isnumeric():
				continue
			synonym_and_def = SynonymAndDef()
			synonym_and_def.word = keyword
			synonym_and_def.synonyms = []
			synonym_and_def.definitions = []
			temp = []
			word = Word(keyword)
			for word in word.get_synsets(pos='n'):
				name = word.lemmas()[0].name()
				if name not in temp:
					synonym_and_def.synonyms.append(name)
					definition = word.definition()
					synonym_and_def.definitions.append(definition)
					if not models.Intrest.objects.filter(keyword__iexact=name).exists():
						intrest = models.Intrest.objects.create(user=user, keyword=name)
						intrest.save()
				temp.append(name)
				having_related_words = True
				having_definitions = True
			words.append(synonym_and_def)
		try_again = False
		no_result_found = False
		link = 'http://gen.lib.rus.ec/search.php?req={0}'.format(search)
		books = []
		try:
			r = requests.get(link)
			bsobj = BeautifulSoup(r.text)
			for tr in bsobj.findAll('table')[2].findAll('tr')[1:]:
				tds = tr.findAll('td')
				author = tds[1].a.get_text()
				all_a = tds[2].findAll('a')
				a = None
				if len(all_a) == 2:
					a = all_a[1]
				else:
					a = all_a[0]
				title = a.contents[0]	
				size = tds[7].get_text()
				extension = tds[8].get_text()
				link = tds[10].a['href']
				new_link = link
				ind = new_link.index
				if new_link[new_link.index(':')-1] != 's':
					new_link = new_link[:new_link.index(':')] + 's' + new_link[new_link.index(':'):]
				book = Book()
				book.title = title
				book.author = author
				book.size = size
				book.extension = extension
				book.link = new_link
				books.append(book)
		except Exception as e:
			print(e)
			try_again = True
		if len(books) == 0:
			no_result_found = True
		context = {
			'books': books,
			'query': search,
			'try_again': try_again,
			'no_result_found': no_result_found,
			'words': words,
			'having_related_words': having_related_words,
			'having_definitions': having_definitions
		}
		return context

	def get(self, request):
		search = request.GET.get('query')
		context = self.parsed(search=search)
		return render(request, 'search-result.html', context=context)

class BookDetail(Search):
	
	def get(self, request, pk):
		book = get_object_or_404(models.Book, id=pk)
		context = self.parsed(search=book.name)
		return render(request, 'search-result.html', context=context)