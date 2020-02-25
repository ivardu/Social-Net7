from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import ugettext, ugettext_lazy as _, ugettext_noop 


def home(request):
	msg = _('Bonjour le monde')
	return HttpResponse(msg)