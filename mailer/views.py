from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin

from django.core.mail import EmailMultiAlternatives as Email
from django.core.mail import get_connection
from django.utils.html import strip_tags
from django.contrib.auth import logout

from mailer import forms

# Create your views here.

class IsSuperUserMixin(UserPassesTestMixin):

	def test_func(self):
		return self.request.user.is_superuser

class Index(IsSuperUserMixin, View):

	def get(self, request):
		return render(request, 'mailer/index.html')

	def post(self, request):
		show_users = request.POST.get('show_users')
		send_email = request.POST.get('send_email')
		log_out = request.POST.get('log_out')
		if show_users:
			emails_json_form = forms.EmailsJson(request.POST, request.FILES)
			if emails_json_form.is_valid():
				html_message = emails_json_form.cleaned_data['html_message']
				return JsonResponse({
						'emails': emails_json_form.cleaned_data['emails_json'],
						'emails_count': len(emails_json_form.cleaned_data['emails_json']),
						'html_message': html_message
					})
			else:
				return JsonResponse({
						'errors': emails_json_form.errors.get_json_data()
					})
		if send_email:		
			mass_mail_form = forms.MassMail(request.POST, request.FILES)
			if mass_mail_form.is_valid():
				plain_message = strip_tags(mass_mail_form.cleaned_data['html_message'])
				html_message = mass_mail_form.cleaned_data['html_message']
				connection = get_connection()
				connection.open()
				email_obj_list = []
				for email in mass_mail_form.cleaned_data['emails_json']:
					email_obj = Email(
							subject=mass_mail_form.cleaned_data['subject'],
							body=plain_message,
							from_email=mass_mail_form.cleaned_data['from_email'],
							to=[email],
							reply_to=['support@librarygenesis.in']
						)
					email_obj.attach_alternative(html_message, 'text/html')
					email_obj_list.append(email_obj)
				connection.send_messages(email_obj_list)
				connection.close()
				return JsonResponse({
						'sent': 1
					})
			else:
				return JsonResponse({
						'errors': mass_mail_form.errors.get_json_data()
					})
		if log_out:
			logout(request)
			return JsonResponse({
					'redirect_page': reverse('index')
				})
		print('nothing executed')