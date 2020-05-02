from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.translation import ugettext, ugettext_lazy as _, ugettext_noop 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from feed.forms import FeedForm, LikesForm, CommentsForm
from feed.models import Feed, Likes, Comments
from users.models import SnetUser

from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic import ListView


@login_required
def feed(request):
	feed = Feed.objects.all()
	feed_form = FeedForm()
	comment_form = CommentsForm()
	page = request.GET.get('page', 1)
	paginator = Paginator(feed, 5)
	# print('stage 1')
	try:
		page_obj = paginator.page(page)

	except PageNotAnInteger:
		page_obj = paginator.page(1)

	except EmptyPage:
		page_obj = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		feed_form = FeedForm(request.POST, request.FILES)
		request_data = (request.FILES.get('image',False) or request.FILES.get('video', False) or request.POST.get('post_info',False))
		# print(request.FILES.get('image',False) or request.FILES.get('video', False) or request.POST.get('post_info',False))
		# print(request.POST.get('video', False ), request_data)
		if feed_form.is_valid() and request_data != False:
			# if len(feed_form.cleaned_data['post_info']) > 0:
			feed_obj = feed_form.save(commit=False)
			feed_obj.user = request.user
			feed_obj.save()
			# print('success')
			return HttpResponseRedirect(reverse('feed:feed'))
		else:
			print(feed_form.errors)

	return render(request, 'feed/feed.html', locals())
	# return HttpResponse('Whats happening')

@login_required
def likes(request, id):
	try:
		feed = Feed.objects.get(pk=id)
		user_liked = Likes.objects.filter(user=request.user).filter(feed=feed)
	except Exception as e:
		print(e)

	if request.method == 'POST':
		likes_form = LikesForm(request.POST)
		if likes_form.is_valid():
			if len(user_liked)==0:
				likes_obj = likes_form.save(commit=False)
				# likes_obj.likes = 1
				likes_obj.feed = feed
				likes_obj.user = request.user
				likes_obj.save()

			else:
				user_liked[0].delete()

			data = {
				'count': feed.likes_set.count()
			}
			# print('working')
			return JsonResponse(data)

			# return HttpResponseRedirect(reverse('feed:feed'))
	else:
		print('Not working')

	# return HttpResponseRedirect(reverse('feed:feed'))

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
			value = (request.user == comment_obj.user)
			# print(value)
			def return_value(value):
				if value:
					return reverse('profile')
				return reverse('rprofile', args=(comment_obj.user.id,))
			# ret_val = return_value(value)	
			# print(comment_obj.comments, comment_obj.user.truncate(),comment_obj.feed.id, comment_obj.user.fname_empty())
			data = {
				'comments':comment_obj.comments,
				'value' : value,
				'user':comment_obj.user.truncate().capitalize(),
				'feed_id': comment_obj.feed.id,
				'fname_empty':comment_obj.user.fname_empty(),
				'url_val': return_value(value),
				'id':'#Feed'+str(comment_obj.feed.id),
			}
			# item.user.truncate|title
			# return HttpResponseRedirect(reverse('feed:feed'))
			return JsonResponse(data)
	else:
		print('Comments Not Working')

	# return HttpResponseRedirect(reverse('feed:feed'))
 
@method_decorator(login_required, name='dispatch')
class MyPostList(ListView):
	template_name = 'feed/myposts.html'
	paginate_by = 5
	model = Feed
	context_object_name = 'feed'

	def get_queryset(self, *args, **kwargs):
		user = SnetUser.objects.get(id=self.kwargs['pk'])
		return Feed.objects.filter(user=user)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['comment_form'] = CommentsForm
		return context

@method_decorator(login_required, name='dispatch')
class FeedEditView(UpdateView):
	model = Feed
	template_name = 'feed/feed_edit.html'
	fields = ['post_info','image']

@method_decorator(login_required, name='dispatch')
class FeedDeleteView(DeleteView):
	model = Feed
	template_name = 'feed/feed_del.html'
	success_url = reverse_lazy('feed:feed')



