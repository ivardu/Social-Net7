from django import forms
from feed.models import Feed, Likes, Comments


class FeedForm(forms.ModelForm):

	post_info = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':"What's on your mind..? Type here", 'id':'id_post_info' }))
	# image  = forms.ImageField(label='', widget=forms.FileInput(attrs={'id':'id_post_image'}))

	class Meta:
		model = Feed
		fields = ['post_info','image']


class LikesForm(forms.ModelForm):

	class Meta:
		model = Likes
		fields = ['likes']

class CommentsForm(forms.ModelForm):
	comments = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'your comment','class':'form-control-sm p-0'}))

	class Meta:
		model = Comments
		fields = ['comments']