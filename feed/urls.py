from django.urls import path
from feed import views 

app_name = 'feed'

urlpatterns = [
	path('',views.feed, name='feed'),
	path('likes/<int:id>/', views.likes, name='likes'),
	path('comments/<int:id>/', views.comments, name='comments'),
	path('myposts/<int:pk>/', views.MyPostList.as_view(), name='myposts'),
	path('edit/<int:pk>/',views.FeedEditView.as_view(),name='feed_edit'),
	path('del/<int:pk>/',views.FeedDeleteView.as_view(), name='feed_del'),
]

