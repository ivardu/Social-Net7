from django import forms
from django.forms import FileInput
from feed.models import Feed, Likes, Comments, RelatedComments


class FeedForm(forms.ModelForm):

	post_info = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':"What's on your mind..? Type here", 'id':'id_post_info', 'class':'post_submit_action', 'autocomplete':'off' }), required=False)
	image  = forms.ImageField(label='', widget=forms.FileInput(attrs={'id':'id_image'}), required=False)
	video = forms.FileField(label='', widget=forms.FileInput(attrs={'id':'id_video'}), required=False)

	class Meta:
		model = Feed
		fields = ['post_info','image', 'video']


class LikesForm(forms.ModelForm):

	class Meta:
		model = Likes
		fields = ['likes']

class CommentsForm(forms.ModelForm):
	comments = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'your comment','class':'form-control fc-class p-0'}))

	class Meta:
		model = Comments
		fields = ['comments']


class RelatedCommentPost(forms.ModelForm):
	
	class Meta:
		model = RelatedComments
		fields = ['related_comment']


# class FeedPostEdit(forms.ModelForm):
# 	class Meta:
# 		model = Feed
# 		fields = ['post_info','image','video']

# 	def clean(self):
# 		cleaned_data = super().clean()

# 		post_info = cleaned_data.get('post_ino','')
# 		image = cleaned_data.get('image',None)
# 		video = cleaned_data.get('video',None)

# 		return cleaned_data