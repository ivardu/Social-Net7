from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext, ugettext_lazy as _, ugettext_noop 
from django.contrib.auth.decorators import login_required

from feed.forms import FeedForm, LikesForm, CommentsForm
from feed.models import Feed, Likes, Comments
from users.models import SnetUser

from django.views.generic.edit import FormView
from django.views.generic import ListView


@login_required
def feed(request):
	feed = Feed.objects.all()
	feed_form = FeedForm()
	comment_form = CommentsForm()
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
@login_required
def likes(request, id):
	try:
		feed = Feed.objects.get(pk=id)
		user_liked = Likes.objects.filter(user=request.user).filter(feed=feed)
		# print(len(user_liked))
	except Exception as e:
		print(e)

	if request.method == 'POST' and len(user_liked)==0:
		likes_form = LikesForm(request.POST)
		if likes_form.is_valid():
			likes_obj = likes_form.save(commit=False)
			# likes_obj.likes = 1
			likes_obj.feed = feed
			likes_obj.user = request.user
			likes_obj.save()
			# print(likes_obj.feed)
			return HttpResponseRedirect(reverse('feed:feed'))

	return HttpResponseRedirect(reverse('feed:feed'))
@login_required
def comments(request, id):
	try:
		feed = Feed.objects.get(id=id)
	except Exception as e:
		print(e)
	# print(feed)
	if request.method == 'POST':
		comment_form = CommentsForm(request.POST)
		if comment_form.is_valid():
			comment_obj = comment_form.save(commit=False)
			comment_obj.user = request.user
			comment_obj.feed = feed
			comment_obj.save()

			return HttpResponseRedirect(reverse('feed:feed'))

	return HttpResponse('Failing')
 

class MyPostList(ListView):
	template_name = 'feed/myposts.html'
	paginate_by = 5
	model = Feed
	context_object_name = 'feed'

	def get_queryset(self, *args, **kwargs):
		user = SnetUser.objects.get(id=self.kwargs['pk'])
		return Feed.objects.filter(user=user)

	# def get_context_data(self, *args, **kwargs):
	# 	context = super().get_context_data(self, *args, **kwargs)


