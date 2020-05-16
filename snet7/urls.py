"""snet7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetConfirmView, 
    PasswordResetDoneView, PasswordResetCompleteView,
    )
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.settings.INSTALLED_APPS 



urlpatterns = [
    path('admin/', admin.site.urls),
    path('feed/',include('feed.urls')),
    path('',user_views.SignUpView.as_view(), name='register'),
    path('login/',LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('rprofile/<int:id>/', user_views.rprofile, name='rprofile'),
    path('friends_req/<int:id>/', user_views.friends_req, name='friends_req'),
    path('friends_accp/<int:id>/',user_views.friends_accp, name='friends_accp'),
    path('cancl_friend/<int:id>',user_views.cancl_friend, name='cancl_friend'),
    path('search/',user_views.search, name='search'),
    path('friends', user_views.friend_req_received, name='friend_req_received'),
    path('pchange/', user_views.PasswordChange.as_view(), name='pchange'),
    path('pass_reset/', user_views.PasswordReset.as_view(), name='pass_reset'),
    path('pass_reset/done/', 
        PasswordResetDoneView.as_view(template_name='users/pass_reset_done.html'), 
        name='password_reset_done'),
    path('pass_reset/confirm/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('pass_reset/complete', 
        PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
        name='password_reset_complete'),
    path('cover_photo/', user_views.cover_photo, name='cover_pic')
]

if settings.DEBUG:

    #Adding debug toolbar to the project settings 
    import debug_toolbar
    urlpatterns += [path('__debug__/',include(debug_toolbar.urls)),]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # print(urlpatterns)

