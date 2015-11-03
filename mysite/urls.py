"""mysite URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from . import views
from .settings import STATIC_ROOT

urlpatterns = [
    # url(r'^$', views.requires_login(views.IndexView.as_view()), name='index'),
    url(r'^$', views.requires_login(views.indexview), name='index'),
    url(r'^knowtest/', include('knowtest.urls', namespace='knowtest')),
    url(r'^goodbye/$', views.logoutview, name='logout'),
    url(r'^loggedout/$', views.loggedoutview, name='loggedout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),
]
