"""simplemooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<slug>[\w_-]+)/$', views.details, name='details'),
    url(r'^(?P<slug>[\w_-]+)/inscricao/$', views.enrollment, name='enrollment'),
	url(r'^(?P<slug>[\w_-]+)/cancelar-inscricao/$', views.undo_enrollment, name='undo_enrollment'),
    url(r'^(?P<slug>[\w_-]+)/anuncios/$', views.announcements, name='announcements'),
    url(r'^(?P<slug>[\w_-]+)/anuncios/(?P<pk>\d+)/$', views.show_announcement, name='show_announcement'),
    url(r'^(?P<slug>[\w_-]+)/aulas/$', views.lessons, name='lessons'),
    url(r'^(?P<slug>[\w_-]+)/aulas/(?P<pk>\d+)/$', views.lesson, name='lesson'),
    url(r'^(?P<slug>[\w_-]+)/materiais/(?P<pk>\d+)/$', views.material, name='material'),
]