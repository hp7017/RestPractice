from . import models
from django.views import View
from django.http import HttpResponse

# Create your views here.

class CopyUser(View):

	def get(self, request):
		return HttpResponse('mapped.')
