# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from .models import Course
from .forms import ContactCourse

def index(request):
	courses = Course.objects.all()
	template_name = 'courses/index.html'
	return render(request, template_name, {'courses': courses})

def details(request, slug):
	course = get_object_or_404(Course, slug=slug)
	template_name='courses/details.html'
	send_email = False
	if request.method == 'POST':
		form = ContactCourse(request.POST)
		if form.is_valid():
			form.send_mail(course)
			send_email = True
			form = ContactCourse()
	else:
		form = ContactCourse()
	return render(request, template_name, {'course': course, 'form': form, 'send_email': send_email})