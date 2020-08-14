from . import models
from django.views import View
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup
from textblob import Word
from django.db.models import Count, Sum, F, Max
from django.db.models.functions import Lower
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.views.decorators.csrf import csrf_exempt
import hashlib
import hmac
import base64
from django.core.mail import EmailMessage
from django.forms import inlineformset_factory, modelformset_factory, modelform_factory
import json
from random import choice

class Book():
	author = None
	size = None
	extension = None
	md5 = None

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
		if request.user.is_authenticated:
			sponsored_books = models.SponsoredBook.objects.only('id', 'thumbnail', 'redirect_link').filter(keywords__title__in=[intrest.keyword for intrest in request.user.intrests.only('keyword')], status='Online').annotate(points=Count('id')).order_by('-points', '-bid')[:5]
			models.SponsoredBook.objects.filter(id__in=[sponsored_book.id for sponsored_book in sponsored_books]).update(impressions_count=F('impressions_count')+1)
		else:
			sponsored_books = models.SponsoredBook.objects.only('id', 'thumbnail', 'redirect_link').filter(status='Online').annotate(points=Count('id')).order_by('-points', '-bid')[:5]
			models.SponsoredBook.objects.filter(id__in=[sponsored_book.id for sponsored_book in sponsored_books]).update(impressions_count=F('impressions_count')+1)
		context = {
			'user': request.user,
			'sponsored_books': sponsored_books,
			'no_of_blank_spaces': [i for i in range(6 - sponsored_books.count())]
		}
		return render(request, 'index.html', context=context)

class Profile(LoginRequiredMixin, View):

	def get(self, request):
		user = User.objects.filter(id=request.user.id).prefetch_related('evaluations', 'books', 'of_profile', 'sponsored_books', 'sponsored_books__keywords')
		user = user[0]
		context = {
			'user' : user,
		}
		return render(request, 'profile.html', context=context)

	def post(self, request):
		if request.POST.get('delete'):
			self.delete_sponsored_book(id_=request.POST.get('sponsored_book_id'))

		if request.POST.get('update'):
			SponsoredBookForm = modelform_factory(models.SponsoredBook, fields=['bid', 'status'])
			sponsored_book_form = SponsoredBookForm(data={'id':id_, 'bid':bid, 'status': status}, instance=models.SponsoredBook.objects.get(id=id_))
			if sponsored_book_form.is_valid():
				sponsored_book = sponsored_book_form.save(commit=False)
				if request.user.of_profile.wallet >= sponsored_book.bid:
					sponsored_book.status = 'Online'
				sponsored_book.save()
			else:
				errors = sponsored_book_form.errors.get_json_data()
				email = EmailMessage(
					subject='[Profile>update_sponsored_book]Undesired error occured',
					body=f'{errors}',
					from_email='Django Server <server@librarygenesis.in>',
					to=['himanshu.pharawal@librarygenesis.in'])
				email.send()
		return redirect(reverse('profile'))

	def delete_sponsored_book(self, id_):
		sponsored_book = models.SponsoredBook.objects.get(id=id_).delete()
		return HttpResponse('done')

class Disclaimer(View):

	def get(self, request):
		return render(request, 'disclaimer.html')

class Search(View):
	'''When exception occur list out of index it might be cause of redire link.'''

	def parsed(self, search, user=None):
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
			for word in word.get_synsets(pos='n'):
				name = word.lemmas()[0].name()
				if name not in temp:
					synonym_and_def.synonyms.append(name)
					definition = word.definition()
					synonym_and_def.definitions.append(definition)
					if user:
						if not models.Intrest.objects.filter(keyword__iexact=name, user=user).exists():
							intrest = models.Intrest(user=user, keyword=name)
							intrest.clean()
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
			with open('proxies.json') as f:
				proxies = json.loads(f.read())
			with open('headers.json') as f:
				headers = choice(json.loads(f.read()))
			proxy = choice(proxies)
			r = requests.get(link, proxies={'http': proxy}, headers=headers)
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
				book.md5 = new_link[new_link.index('=')+1:]
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
		if request.user.is_authenticated:
			search_model = models.Search(search=search, user=request.user)
			search_model.save()
			context = self.parsed(search=search, user=request.user)
		else:
			context = self.parsed(search=search)
		return render(request, 'search-result.html', context=context)

class BookDetail(Search):
	
	def get(self, request, pk, slug):
		book = get_object_or_404(models.Book, id=pk)
		context = self.parsed(search=book.name)
		return render(request, 'search-result.html', context=context)

class Evaluation(LoginRequiredMixin, View):

	def get(self, request):
		user = User.objects.filter(id=request.user.id).prefetch_related('books')
		context = {
			'user': user[0],
		}
		return render(request, 'unavailable.html', context=context)

	def post(self, request):
		pk = request.POST.get('books')
		book = models.Book.objects.get(id=pk)
		title = request.POST.get('title')
		link = request.POST.get('link')
		models.Evaluation.objects.create(book=book, title=title, link=link)
		return redirect(reverse('evaluations'))

class AdsManager(LoginRequiredMixin, View):

	def get(self, request):
		if models.Profile.objects.filter(user_id=request.user.id).exists():
			profile = models.Profile.objects.get(user_id=request.user.id)
			profile_form = forms.ProfileForm(instance=profile)
		else:
			profile_form = forms.ProfileForm()
		keyword_formset = inlineformset_factory(models.SponsoredBook, models.Keyword, form=forms.KeywordForm, can_delete=False, extra=5, max_num=5, min_num=1, validate_max=True, validate_min=True, formset=forms.KeywordFormset)
		context = {
			'profile_form': profile_form,
			'keyword_formset': keyword_formset
		}
		return render(request, 'ads-manager.html', context=context)

	def post(self, request):
		sponsored_book_form = forms.SponsoredBookForm(request.POST, request.FILES)
		keywords_formset = inlineformset_factory(models.SponsoredBook, models.Keyword, form=forms.KeywordForm, can_delete=False, max_num=5, min_num=1, validate_max=True, validate_min=True, formset=forms.KeywordFormset)
		if models.Profile.objects.filter(user_id=request.user.id).exists():
			profile = models.Profile.objects.get(user_id=request.user.id)
			profile_form = forms.ProfileForm(request.POST, instance=profile)
		else:
			profile_form = forms.ProfileForm(request.POST)
		if sponsored_book_form.is_valid():
			sponsored_book = sponsored_book_form.save(commit=False)
			keywords_formset = keywords_formset(request.POST, instance=sponsored_book)
			if keywords_formset.is_valid():
				sponsored_book.user_id = request.user.id
				if profile_form.is_valid():
					profile = profile_form.save(commit=False)
					profile.user_id = request.user.id
					profile.save()
					sponsored_book.save()
					keywords_formset.save()
					return JsonResponse({'is_submit': True})
					
				else:
					errors = profile_form.errors.get_json_data()
			else:
				errors = keywords_formset.get_json_data()
				for form in keywords_formset:
					errors.update(form.errors.get_json_data())		
		else:
			errors = sponsored_book_form.errors.get_json_data()

		return JsonResponse({'errors':errors})

class SponsoredBookClicked(View):

	def post(self, request):
		sid = request.POST.get('sid')
		sponsored_books = models.SponsoredBook.objects.filter(id=sid).select_related('user', 'user__of_profile')
		sponsored_book = sponsored_books[0]
		if sponsored_book.user.of_profile.balance < sponsored_book.bid:
			email = EmailMessage(
				subject='Balance insufficient',
				body=f'You have got a click on you book. But due to insufficient balance in your wallet your book titled as {sponsored_book.title} is no more visible on sponsored section.\n\nPlease recharge your wallet to continue promoting your book. Visit {request.scheme}://{request.get_host()}/profile and recharge your wallet.\n\nThanks and Regards,\nLibrary Genesis App',
				from_email='My Wallet <wallets@librarygenesis.in>',
				reply_to=['support@librarygenesis.in'],
				to=[sponsored_book.user.email])
			email.send()
			sponsored_book.status = 'Insufficient-Balance'
			sponsored_book.save()
		else:
			sponsored_book.engadgements_count += 1
			sponsored_book.user.of_profile.balance -= sponsored_book.bid
			sponsored_book.user.of_profile.save()
			sponsored_book.save()
		return HttpResponse('ok.')

class KeywordPlannerClicked(LoginRequiredMixin, View):

	def get(self, request):
		keyword = request.GET.get('keyword')
		if keyword:
			if not len(keyword.split(' ')) > 1:
				keyword = keyword.lower()
				estimated_traffic = int((User.objects.filter(intrests__keyword=keyword).count()/User.objects.count())*100)
				estimated_bid = models.SponsoredBook.objects.filter(keywords__title=keyword).aggregate(Max('bid'))
				if not estimated_bid['bid__max']:
					estimated_bid['bid__max'] = 5
				return JsonResponse({'estimated_traffic': estimated_traffic, 'estimated_bid': estimated_bid['bid__max']+2})
			else:
				return JsonResponse({'error': 'You can not use spaces. It is suppose to analyse a single keyword'})
		else:
			return JsonResponse({'error': 'Please enter a keyword'})

class RechargeClicked(View, LoginRequiredMixin):

	def get(self, request):
		amount = request.GET.get('amount')
		if float(amount) >= 5:
			user = User.objects.filter(id=request.user.id).prefetch_related('of_profile')
			user = user[0]
			order = models.Order.objects.create(user=user, amount=amount)
			#cashfree
			host = request.get_host()
			postData = {
				"appId" : '21675bd6ae0fb1336e5c8d2d957612',
				"orderId": str(order.id),
				"orderAmount" : str(amount),
				"orderCurrency" : 'INR',
				"orderNote" : '*Non-indian users can pay only with Paypal',
				"customerName" : str(user.username),
				"customerPhone" : str(user.of_profile.phone),
				"customerEmail" : str(user.email),
				"returnUrl" : 'https://'+host+reverse('payment_return'),
				"notifyUrl" : 'https://'+host+reverse('payment_done'),
			}
			sortedKeys = sorted(postData)
			signatureData = ""
			for key in sortedKeys:
				signatureData += key+postData[key]
			message = signatureData.encode('utf-8')
			secret = 'c9de14e9a061a679737a9a3b7edf2f03519ccc82'.encode('utf-8')
			signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest()).decode('utf-8')
			#end cashfree
			return JsonResponse({
				"signature": signature,
				"appId" : postData['appId'],
				"orderId": postData['orderId'],
				"orderAmount" : postData['orderAmount'],
				"orderCurrency" : postData['orderCurrency'],
				"orderNote" : postData['orderNote'],
				"customerName" : postData['customerName'],
				"customerPhone" : postData['customerPhone'],
				"customerEmail" : postData['customerEmail'],
				"returnUrl" : postData['returnUrl'],
				"notifyUrl" : postData['notifyUrl']
				})
		else:
			return JsonResponse({
				'error': 'amount must be greater than or equals to INR 5.'
				})


@csrf_exempt
def payment_done(request):
	orderId = request.POST.get('orderId')
	orderAmount = request.POST.get('orderAmount')
	referenceId = request.POST.get('referenceId')
	txStatus = request.POST.get('txStatus')
	paymentMode = request.POST.get('paymentMode')
	txMsg = request.POST.get('txMsg')
	txTime = request.POST.get('txTime')
	order = models.Order.objects.filter(id=orderId).select_related('user', 'user__of_profile').prefetch_related('user__sponsored_books')
	order = order[0]
	print(order.user.__dict__)
	order.amount = orderAmount
	order.reference_id = referenceId
	order.status = txStatus
	order.payment_mode = paymentMode
	order.tx_msg = txMsg
	order.tx_time = txTime
	OrderForm = modelform_factory(models.Order, exclude=['user'])
	order_form = OrderForm(data={
		'amount': orderAmount,
		'reference_id': referenceId,
		'status': txStatus,
		'payment_mode': paymentMode,
		'tx_msg': txMsg,
		'tx_time': txTime
		}, instance=order)
	if order_form.is_valid():
		order_form.save()
		order.user.of_profile.balance += float(orderAmount)
		order.user.of_profile.save()
		order.user.sponsored_books.filter(bid__lt=order.user.of_profile.balance).update(status='Online')
		email = EmailMessage(
			subject='Payment successful.',
			body=f'You have made a successfull payment of INR {order.amount} to your wallet.\nYou can see the transaction related information below:\namount: {order.amount},\nreference_id: {order.reference_id},\nstatus: {order.status},\npayment_mode: {order.payment_mode},\ntransaction time: {order.tx_time},\n\nIf you found something wrong please let us know at support@librarygenesis.in\n\nThanks and Regards,\nLibrary Genesis App',
			from_email='My Wallet <wallets@librarygenesis.in>',
			to=[order.user.email])
		email.send()
	else:
		email = EmailMessage(
			from_email='Django Server <server@librarygenesis.in>',
			body=f'validation error occured\nvalidation = {order_form.errors.get_json_data()}\nrequest.uses.id = {request.user.id}',
			subject='[Emergency Payment]validation error occured',
			to=['himanshu.pharawal@librarygenesis.in'])
		email.send()
	return HttpResponse('ok.')

@csrf_exempt
def payment_return(request):
	orderId = request.POST.get('orderId')
	orderAmount = request.POST.get('orderAmount')
	referenceId = request.POST.get('referenceId')
	txStatus = request.POST.get('txStatus')
	paymentMode = request.POST.get('paymentMode')
	txMsg = request.POST.get('txMsg')
	txTime = request.POST.get('txTime')
	if txStatus != 'SUCCESS':
		order = models.Order.objects.get(id=orderId)
		order.amount = orderAmount
		order.reference_id = referenceId
		order.status = txStatus
		order.payment_mode = paymentMode
		order.tx_msg = txMsg
		order.tx_time = txTime
		OrderForm = modelform_factory(models.Order, exclude=['user'])
		order_form = OrderForm(data={
			'amount': orderAmount,
			'reference_id': referenceId,
			'status': txStatus,
			'payment_mode': paymentMode,
			'tx_msg': txMsg,
			'tx_time': txTime
			}, instance=order)
		if order_form.is_valid():
			order_form.save()
		else:
			email = EmailMessage(
				from_email='Django Server <server@librarygenesis.in>',
				body=f'validation error occured\nvalidation = {order_form.errors.get_json_data()}\nrequest.uses.id = {request.user.id}',
				subject='[Emergency]validation error occured',
				to=['himanshu.pharawal@librarygenesis.in'])
			email.send()
	context = {
		'orderId': orderId,
		'orderAmount': orderAmount,
		'txStatus': txStatus,
		'txMsg': txMsg
	}
	return render(request, 'payment_return.html', context=context)

class ContactUs(View):

	def get(self, request):
		return render(request, 'contact_us.html')

	def post(self, request):
		text = request.POST.get('msg')
		email = request.POST.get('email')
		if text and email:
			msg = models.Msg.objects.create(email=email, text=text)
			return HttpResponse(f'Thanks for contacting us. If it was a question we will get back to you soon. Token number is {msg.id}')
		else:
			models.Msg.objects.create(email='self@librarygenesis.in', text='Contact Us page is not working! text or email have recieved as none instead of object.\nemail = {email}\ntext = {text}')
			return HttpResponse('Somthing went wrong! Report has been sent.')

class BookClicked(LoginRequiredMixin, View):

	def handle_no_permission(self):
		return HttpResponse(reverse('login'))

	def get(self, request):
		prefix = 'https://libgen.lc/ads.php?md5='
		md5 = request.GET.get('id')
		if md5:
			link = prefix + md5
			try:
				response = requests.get(link)
				bsobj = BeautifulSoup(response.text)
				final_link = bsobj.find('table').findAll('tr')[0].findAll('td')[1].a['href']
			except Exception as e:
				email = EmailMessage(
					subject='Book download link was not received',
					body=f'class = BookClicked\nmethod = get\ncomplete error = {e}',
					from_email='Django Server <server@librarygenesis.in>',
					to=['himanshu.pharawal@librarygenesis.in'])
				email.send()
			return HttpResponse(final_link)
		else:
			email = EmailMessage(
				subject='md5 was received as null',
				body=f'class = BookClicked\nmethod = get',
				from_email='Django Server <server@librarygenesis.in>',
				to=['himanshu.pharawal@librarygenesis.in'])
			email.send()
			return HttpResponse(reverse('oops'))

class Oops(View):

	def get(self, request):
		return render(request, 'oops.html')

class Registration(View):

	def get(self, request):
		registration_form = forms.RegistrationForm()
		return render(request, 'registration/registration.html', context={'registration_form': registration_form})

	def post(self, request):
		from django.contrib.auth import login
		registration_form = forms.RegistrationForm(request.POST)
		if registration_form.is_valid():
			user = registration_form.save()
			login(request, user)
			email = EmailMessage(
				subject='Sucessfully created account',
				body=f'Welcome to Library Genesis App. You have successfully created your account.\n\nNow you can enjoy downloading books absoluetly free.\nIf you are a writer or blogger who wants to promote his/her book or article then you are very welcome to ads-manager service by us. Please visit {request.scheme}://{request.get_host()}/ads-manager for more info.\n\nIf you have not created this account please reply this email or let us know the issue at support@librarygenesis.in\n\nThanks and Regards,\nLibrary Genesis App',
				reply_to=['support@librarygenesis.in'],
				from_email='Accounts <accounts@librarygenesis.in>',
				to=[request.user.email])
			email.send()
			return redirect(reverse('profile'))
		return render(request, 'registration/registration.html', context={'registration_form': registration_form})

def our_policy(request):
	return render(request, 'our_policy.html')

def terms_condition(request):
	return render(request, 'terms_condition.html')

def about_us(request):
	return render(request, 'about_us.html')