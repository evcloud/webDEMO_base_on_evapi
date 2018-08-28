"""innervm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.i18n import javascript_catalog
from interclient.views import index
from django.views.static import serve

urlpatterns = [

    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', javascript_catalog,  name='javascript-catalog'), 
    url(r'^$', index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^interclient/', include('interclient.urls')),

]

urlpatterns += [
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
