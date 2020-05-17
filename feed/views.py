from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.translation import ugettext, ugettext_lazy as _, ugettext_noop 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from feed.forms import FeedForm, LikesForm, CommentsForm, RelatedCommentPost
# , FeedPostEdit
from feed.models import Feed, Likes, Comments, CommentLikes, RelatedComments, RelatedCommentsLikes
from users.models import SnetUser

from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.decorators.csrf import ensure_csrf_cookie


@login_required
def feed(request):
	luser = request.user
	feed =  Feed.objects.filter(Q(Q(user__friends__freq_usr=luser)|Q(user__friends__freq_accp=luser), user__friends__friends='Yes')|Q(user=luser)).distinct()
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
		feed = None
	# print(feed)
	if request.method == 'POST' and feed:
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
				'user':comment_obj.user.truncate(),
				'feed_id': comment_obj.feed.id,
				'fname_empty':comment_obj.user.fname_empty(),
				'url_val': return_value(value),
				'id':'#Feed'+str(comment_obj.feed.id),
				'oid':comment_obj.id
			}
			# item.user.truncate|title
			# return HttpResponseRedirect(reverse('feed:feed'))
			return JsonResponse(data)
	else:
		print('Comments Not Working')

	# return HttpResponseRedirect(reverse('feed:feed'))

@login_required
def comment_update(request, id):
	try:
		comment_instance = Comments.objects.get(id=id)
		# print(request.POST)
	except Exception as e:
		comment_instance = None

	if request.method == 'POST' and comment_instance:
		comment_update_form = CommentsForm(request.POST, instance=comment_instance)
		if comment_update_form.is_valid():
			obj = comment_update_form.save()

			data = {'comment_val':obj.comments}

			return JsonResponse(data) 
	# 	else:
	# 		print(comment_update_form.errors)
	# else:
	# 	print(request.method, comment_instance)


@login_required
def related_comments(request, id):
	try:
		related_comment_parent_inst = Comments.objects.get(pk=id)
	except:
		related_comment_parent_inst = None

	if request.method == 'POST' and related_comment_parent_inst:
		print('Yes its a post..',related_comment_parent_inst, request.method)
		related_comment_form = RelatedCommentPost(request.POST)
		if related_comment_form.is_valid():
			print('form is valid')
			rcomment_obj = related_comment_form.save(commit=False)
			rcomment_obj.parent_comment = related_comment_parent_inst
			rcomment_obj.user = request.user
			rcomment_obj.save()

			data = {
				'comments':rcomment_obj.related_comment,
				'a_value':request.user.truncate(),
				'id':rcomment_obj.id,
			}
			return JsonResponse(data)
		else:
			print(related_comment_form.errors)

	else:
		print('failing')


@login_required
def related_comments_update(request, id):
	try:
		rc_obj = RelatedComments.objects.get(pk=id)
	except:
		rc_obj = None
	print(rc_obj)

	if request.method == 'POST' and rc_obj:
		rc_form = RelatedCommentPost(request.POST, instance=rc_obj)
		if rc_form.is_valid():

			rc_m_obj = rc_form.save()
			uc_data = {
				'rc' : rc_m_obj.related_comment
			}
			return JsonResponse(uc_data)
		else:
			print(rc_form.errors)

@login_required
def comment_likes(request, id):
	try:
		comment_obj = Comments.objects.get(pk=id)
		current_value = CommentLikes.objects.filter(like_parent=comment_obj, user=request.user)
		print(comment_obj, request.method, current_value)
	except:
		comment_obj = None
		# print('here..!!')

	if request.method == 'POST':
		if comment_obj != None and current_value and current_value[0].likes == 1:
			print('Am I in..!!')
			current_value[0].delete()
		else:
			CommentLikes.objects.create(likes=1, user=request.user, like_parent=comment_obj)

		data = {
			'likes':comment_obj.commentlikes_set.count()
		}
	else:
		print('failing')

	return JsonResponse(data)


@login_required
def realted_comment_likes(request, id):
	try:
		rcomment_obj = RelatedComments.objects.get(pk=id)
		print(rcomment_obj)
		rcurrent_value = RelatedCommentsLikes.objects.filter(rc_like_parent=rcomment_obj, user=request.user)
		print(rcomment_obj, request.method, rcurrent_value)
	except:
		rcomment_obj = None
		# print('here..!!')

	if request.method == 'POST':
		if rcomment_obj != None and rcurrent_value and rcurrent_value[0].likes == 1:
			print('Am I in..!!')
			rcurrent_value[0].delete()
		else:
			RelatedCommentsLikes.objects.create(likes=1, user=request.user, rc_like_parent=rcomment_obj)

		data = {
			'likes':rcomment_obj.relatedcommentslikes_set.count()
		}
	else:
		print('failing')

	return JsonResponse(data)

 
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
	# template_name = 'feed/feed_edit.html'
	fields = ['post_info','image','video']
	# form_class=FeedPostEdit
	def result(self):
		self.object = self.get_object()
		# print(self.object)
		image = ['' if self.object.image == '' else self.object.image.url]
		video = ['' if self.object.video == '' else self.object.video.url]
		data = {
			'image':image[0],
			'video':video[0],
			'post_info':self.object.post_info
		}
		return data

	# def form_valid()

	def form_valid(self, form):
		self.object = form.save()
		data = self.result()
		return JsonResponse(data)

	def get(self, request, *args, **kwargs):
		data = self.result()
		return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class FeedDeleteView(DeleteView):
	model = Feed
	template_name = 'feed/feed_del.html'
	success_url = reverse_lazy('feed:feed')



