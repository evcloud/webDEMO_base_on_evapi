 
from django.conf.urls import include, url
from .views import *
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', index),
    url(r'^login/$',  login, {'template_name':'accounts_login.html'}), 
    url(r'^logout/$', logout),
    url(r'^register/$', register),
    url(r'^confirm/$', confirm),
    url(r'^passwdreset/$',passwd_reset),
    url(r'^passwdfind/$',passwd_find),
    url(r'^passwdfindconfirm/$',passwd_find_confirm),
]
