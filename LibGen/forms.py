from django import forms
from django.forms import ModelForm, Form, BaseInlineFormSet
from . import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SponsoredBookForm(ModelForm):
		
	class Meta:
		model = models.SponsoredBook
		fields = ['status', 'bid']

	def clean_placed_on(self):
		placed_on = self.cleaned_data['placed_on']
		if placed_on != 'Royal-Place':
			raise ValidationError('Only Royal Place(Recommended section on home page) is available right now.')
		return placed_on

class KeywordForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['title'].widget.attrs['class'] = 'section__form__fieldset--keyword__div--wrap__input'

	class Meta:
		model = models.Keyword
		fields = '__all__'

class KeywordFormset(BaseInlineFormSet):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		form = self.forms[0]
		form.fields['title'].widget.attrs['required'] = "true"

	def clean(self):
		super().clean()
		titles = []
		for form in self.forms:
			try:
				if form.cleaned_data['title'] in titles:
					raise ValidationError('Keywords can not be same in two fields. Please use different keywords')
				else:
					titles.append(form.cleaned_data['title'])
			except KeyError as e:
				pass

	def get_json_data(self):
		messages = []
		for error in self.non_form_errors():
			messages.append({'message': error})
		return {'keywords' : messages}

class ProfileForm(ModelForm):
	class Meta:
		model = models.Profile
		fields = ['phone']

class RegistrationForm(UserCreationForm):
	email = forms.CharField(widget=forms.EmailInput)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class EmailDashboardForm(forms.Form):
	from_email = forms.CharField(widget=forms.EmailInput, required=False)
	to = forms.CharField()
	cc = forms.CharField(required=False)
	subject = forms.CharField()
	body = forms.CharField(widget=forms.Textarea)

	def clean_from_email(self):
		return 'Notification <notify@librarygenesis.in>'