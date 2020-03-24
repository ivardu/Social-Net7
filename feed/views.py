from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext, ugettext_lazy as _, ugettext_noop 
from django.contrib.auth.decorators import login_required
from feed.forms import FeedForm, LikesForm
from feed.models import Feed
from django.views.generic.edit import FormView


@login_required
def feed(request):
	feed = Feed.objects.all()
	feed_form = FeedForm()
	if request.method == 'POST':
		feed_form = FeedForm(request.POST, request.FILES)
		if feed_form.is_valid():
			feed_obj = feed_form.save(commit=False)
			feed_obj.user = request.user
			feed_obj.save()
			return HttpResponseRedirect(reverse('feed:feed'))
	# else:
		# likes = feed.likes_set.filter(likes=1).count()

	return render(request, 'feed/feed.html', locals())
	# return HttpResponse('Whats happening')

# class Feed(FormView):
# 	form_class = FeedForm
# 	template_name = 'feed/feed.html'

def likes(request, id):
	try:
		feed = Feed.objects.get(pk=id)
	except:
		print('Exception in id of feed model')
	if request.method == 'POST':
		likes_form = LikesForm(request.POST)
		if likes_form.is_valid():
			likes_obj = likes_form.save(commit=False)
			likes_obj.feed = feed
			likes_obj.user = request.user
			likes_obj.save()
			# print(likes_obj.feed)
			return HttpResponseRedirect(reverse('feed:feed'))

	return HttpResponse('hello')

 
