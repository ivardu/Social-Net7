from django import forms
from feed.models import Feed, Likes


class FeedForm(forms.ModelForm):

	post_info = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':"What's on your mind..?"}))

	class Meta:
		model = Feed
		fields = ['post_info','image']


class LikesForm(forms.ModelForm):

	class Meta:
		model = Likes
		fields = ['likes']