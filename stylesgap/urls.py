"""hello URL Configuration

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
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^db/', views.db),

    ##########################################################################
    ######################	ADMIN PANEL URL  #################################
    ##########################################################################

    #***** LOGIN FOR ADMIN ******
    url(r'^dashboard/', views.login),
    
    #***** LOGOUT FOR ADMIN *****
    url(r'^logout/', views.logout),

    #***** VIEW COMMENTS FOR ADMIN *****
    url(r'^view_comment/', views.view_comment),

    #***** CRUD AT CATEGORY *****
    url(r'^add_category/', views.add_category),
    url(r'^view_category/', views.view_category),
    url(r'^delete_category/(?P<id>\d+)/$', views.delete_category),
    url(r'^edit_category/(?P<id>\d+)/$', views.edit_category),

    #***** CRUD AT POST *****
    url(r'^add_post/', views.add_post),
    url(r'^view_post/', views.view_post),
    url(r'^delete_post/(?P<id>\d+)/$', views.delete_post),
    url(r'^edit_post/(?P<id>\d+)/$', views.edit_post),

    

    ##########################################################################
    ######################	FRONT-END URL  ###################################
    ##########################################################################

    #***** INDEX PAGE *****
    url(r'^$', views.index),

    #***** BLOG PAGE *****
    url(r'^blog/', views.blog),

    #***** BLOG PAGE *****
    url(r'^contact/', views.contact),

    #***** BLOG DETAIL PAGE *****
    url(r'^blogdetail/(?P<id>\d+)/$', views.blogdetail),

    #***** POST AGAINST CATEGORY PAGE *****
    url(r'^catpost/(?P<id>\d+)/$', views.catpost),
]
