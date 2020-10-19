from django.conf.urls import include, url
from home.views import index_view,download_view,about_view,search_view, ajax_mirna, ajax_mirtarbase, view_all
"""miRATBase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'download', download_view, name="Downloads"),
    url(r'about', about_view, name="About"),
    url(r'search', search_view, name="search"),
    url(r'ajax_mirna', ajax_mirna, name="ajax_mirna"),
    url(r'ajax_mirtar', ajax_mirtarbase, name="ajax_mirtar"),
    url(r'all', view_all, name="all"),
    url(r'^/*$', index_view, name='home'),

]
