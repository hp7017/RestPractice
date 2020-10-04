from django import forms
from django.core.exceptions import ValidationError

import json

class UserEmail(forms.Form):
	email = forms.EmailField()

class EmailsJson(forms.Form):
	emails_json = forms.FileField()
	html_message = forms.FileField()

	def clean_emails_json(self):
		data = self.cleaned_data['emails_json']
		if data.name.split('.')[-1] != 'json':
			raise ValidationError('Emails file must be json format')
		emails = json.loads(data.read())
		try:
			emails = [email0['email'] for email0 in emails]
			return emails
		except Exception as e:
			raise ValidationError(f'{data.name} is not in required format')

	def clean_html_message(self):
		data = self.cleaned_data['html_message']
		if data.name.split('.')[-1] != 'html':
			raise ValidationError('Message file should be html format')
		dat = data.read()
		da = [chr(c) for c in dat]
		html_message = ''.join(da)
		return html_message

class MassMail(EmailsJson):
	from_email = forms.ChoiceField(
			choices=(
					('Notification <notify@librarygenesis.in>', 'Notification'),
					('Pradum Kumar', 'Pradum Kumar <pradum.kumar@librarygenesis.in>')
				)
		)
	subject = forms.CharField()