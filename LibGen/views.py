from . import models
from django.views import View
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup
from textblob import Word

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

class Index(View):

	def get(self, request):
		return render(request, 'index.html')

class Profile(View):

	def get(self, request):
		return render(request, 'profile.html')

class Disclaimer(View):

	def get(self, request):
		return render(request, 'disclaimer.html')

class Search(View):

	def get(self, request):
		search = request.GET.get('query')
		words = []
		having_related_words = False
		having_definitions = False
		keywords = search.split(' ')
		for keyword in keywords:
			if len(keyword) == 1 or keyword.isnumeric():
				continue
			synonym_and_def = SynonymAndDef()
			synonym_and_def.word = keyword
			synonym_and_def.synonyms = []
			synonym_and_def.definitions = []
			temp = []
			word = Word(keyword)
			synsets = word.get_synsets(pos='n')
			for syn in word.get_synsets(pos='v'):
				synsets.append(syn)
			print(synsets)
			for word in synsets:
				name = word.lemmas()[0].name()
				if name not in temp:
					synonym_and_def.synonyms.append(name)
					definition = word.definition()
					synonym_and_def.definitions.append(definition)
				temp.append(name)
				having_related_words = True
				having_definitions = True
			words.append(synonym_and_def)
		user = User.objects.get(pk=3)
		try_again = False
		no_result_found = False
		search_model = models.Search.objects.create(search=search, user=user)
		search_model.save()
		link = 'http://gen.lib.rus.ec/search.php?req={0}'.format(search)
		r = requests.get(link)
		bsobj = BeautifulSoup(r.text)
		books = []
		try:
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
		return render(request, 'search-result.html', context=context)

class BookDetail(View):
	
	def get(self, request, pk):
		return HttpResponseRedirect(reverse('search/?search={0}'.format))