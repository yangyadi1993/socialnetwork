"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from . import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add$', views.add_profile, name='add'),
    #url(r'^edit-profile/(?P<id>\d+)$', views.edit_profile, name='edit'),
    url(r'^login$', login, {'template_name': 'grumblr/login.html'}, name='login'),
    url(r'^logout$', logout_then_login, name='logout'),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^profile$', views.myProfile, name='myProfile'),
    url(r'^global$', views.globalPage, name='global'),
    url(r'^follower$', views.follower_stream, name='follower'),
    url(r'^add_post$', views.add_post, name='post'),
    # url(r'^add_comment/(?P<id>\d+)$', views.add_comment, name='comment'),
    url(r'^add_comment$', views.add_comment, name='comment'),
    url(r'^get_posts/?$', views.get_posts, name='get_posts'),
    url(r'^get_follower_posts/?$', views.get_follower_posts),
    url(r'^get_myprofile_posts/?$', views.get_myprofile_posts),
    url(r'^get_profile_posts/?$', views.get_profile_posts),
    url(r'^get_posts/(?P<time>.+)$', views.get_posts),
    url(r'^get_changes/?$', views.get_changes, name='get_changes'),
    url(r'^get_changes/(?P<time>.+)$', views.get_changes),
    url(r'^follow(?P<userid>\d+)/$', views.follow_other, name='follow_other'),
    url(r'^unfollow(?P<userid>\d+)/$', views.unfollow, name='unfollow'),
    #url(r'^user/password/reset/$', password_reset, {'post_reset_redirect': '/user/password/reset/done/'}, name='password_reset'),
    #url(r'^user/password/reset/$', password_reset, {'template_name': 'grumblr/registration/password_reset_form.html', 'post_reset_redirect': '/user/password/reset/done/'}, name='password_reset'),
    url(r'^user/password/reset/$', views.password_reset, name='password_reset'),
    url(r'^user/password/reset/done/$', password_reset_done, {'template_name': 'grumblr/registration/password_reset_done.html'}),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'template_name': 'grumblr/registration/password_reset_confirm.html','post_reset_redirect': '/user/password/done/'}, name='password_reset_email'),
    url(r'^user/password/done/$', password_reset_complete, {'template_name': 'grumblr/registration/password_reset_complete.html'}),
    url(r'^confirm/(?P<username>[a-z_0-9.-]{1,64}@([a-z0-9-]{1,200}.){1,5}[a-z]{1,6})/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.confirm_registration, name='confirm'),
    url(r'^edit_profile/(?P<id>\d+)/$', views.edit_profile, name='edit'), 
    url(r'^edit_password/(?P<id>\d+)/$', views.edit_password, name='edit_password'),   
    url(r'^profile/(?P<userid>\d+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<userid>\d+)/photo/(?P<id>\d+)/$', views.get_photo_profile),
    url(r'^photo/(?P<id>\d+)/$', views.get_photo, name='photo'),
    url(r'^photo/$', views.get_photo, name='photo')
]

# import os
# if settings.DEBUG404:
#     urlpatterns += url('',
#     (r'^static/(?P<path>.*)$', 'django.views.static.serve',
#     {'document_root': os.path.join(os.path.dirname(__file__), 'static')} ),
#     )