from django.urls import path
from feed import views 

app_name = 'feed'

urlpatterns = [
	path('',views.feed, name='feed'),
	path('likes/<int:id>/', views.likes, name='likes'),
	path('comments/<int:id>/', views.comments, name='comments'),
	path('comment_update/<int:id>/', views.comment_update, name='comment_update'),
	path('myposts/<int:pk>/', views.MyPostList.as_view(), name='myposts'),
	path('edit/<int:pk>/',views.FeedEditView.as_view(),name='feed_edit'),
	path('del/<int:pk>/',views.FeedDeleteView.as_view(), name='feed_del'),
	path('rc/<int:id>/', views.related_comments, name='related_comment'),
	path('cl/<int:id>/',views.comment_likes, name='comment_likes'),

]

