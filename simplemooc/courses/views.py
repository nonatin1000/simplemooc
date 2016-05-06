# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from .models import Course

def index(request):
	courses = Course.objects.all()
	template_name = 'courses/index.html'
	return render(request, template_name, {'courses': courses})

def details(request, slug):
	course = get_object_or_404(Course, slug=slug)
	template_name='courses/details.html'
	return render(request, template_name, {'course': course})