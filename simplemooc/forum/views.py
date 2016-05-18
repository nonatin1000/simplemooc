# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView

from .models import Thread

class ForumView(ListView):

	model = Thread
	paginate_by = 4
	template_name = 'forum/index.html'

index = ForumView.as_view()