from django import forms
from django.forms import ModelForm, Form
from django.forms import inlineformset_factory, modelformset_factory
from . import models
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from django.core.validators import MinValueValidator

class KeywordForm(ModelForm):
	class Meta:
		mdoel = models.Keyword
		exclude = ['impressions_count']

	def __init__(self, *args, **kwargs):
		super(KeywordForm, self).__init__(*args, **kwargs)
		self.fields['title'].widget.attrs['required'] = ''

class keyword_form_set(inlineformset_factory(models.SponsoredBook, models.Keyword, form=KeywordForm ,extra=5, max_num=5, can_delete=False)):
	def clean(self):
		super().clean()
		keywords = []
		for form in self.forms:
			new = form.cleaned_data['title'].lower()
			if len(new.split(' ')) > 1:
				raise ValidationError('Keyword can only be single word. Do not use spaces to seprate keywords use another block instead.')
			if new not in keywords:
				keywords.append(new)
			else:
				raise ValidationError('Keywords(case insenstive) must be unique.')

class SponsoredBookForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(SponsoredBookForm, self).__init__(*args, **kwargs)
		self.fields['bid'].widget.attrs['placeholder'] = 'in USD'
		self.fields['redirect_link'].widget.attrs['placeholder'] = 'eg: https://librarygenesis.com'
		
	class Meta:
		model = models.SponsoredBook
		exclude = ['user', 'engadgements_count', 'impressions_count', 'status']

	def clean_placed_on(self):
		placed_on = self.cleaned_data['placed_on']
		if placed_on != 'Royal-Place':
			raise ValidationError('Only Royal Place(Recommended section on home page) is available right now.')
		return placed_on

class RechargeForm(Form):
	def __init__(self, *args, **kwargs):
		super(RechargeForm, self).__init__(*args, **kwargs)
		self.fields['amount'].widget.attrs['placeholder'] = 'in USD'
	amount = forms.FloatField(validators=[MinValueValidator(0.1)])