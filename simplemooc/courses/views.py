# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment
from django.contrib import messages
from .forms import ContactCourse

def index(request):
	courses = Course.objects.all()
	template_name = 'courses/index.html'
	context = {
		'courses': courses
	}
	return render(request, template_name, context)

def details(request, slug):
	course = get_object_or_404(Course, slug=slug)
	template_name='courses/details.html'
	context = {}
	if request.method == 'POST':
		form = ContactCourse(request.POST)
		if form.is_valid():
			context['is_valid'] = True
			form.send_mail(course)
			form = ContactCourse()
	else:
		form = ContactCourse()

	context['form'] = form
	context['course'] = course
	return render(request, template_name, context)

def enrollment(request, slug):
	course = get_object_or_404(Course, slug=slug)
	enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

	if created:
		enrollment.active()
		messages.sucess(request, 'Você foi inscrito no curso com sucesso.')
	else:
		messages.info(request, 'Você já está inscrito no curso.')

	return redirect('accounts:dashboard')

@login_required
def undo_enrollment(request, slug):
	template_name='courses/undo_enrollment.html'
	course = get_object_or_404(Course, slug=slug)
	enrollment = Enrollment.objects.get_or_create(user=request.user, course=course)
	if request.method == 'POST':
		enrollment.delete()

	context = {
		'enrollment': enrollment,
		'course': course,
	}
	return render(request, template_name, context)

@login_required
def announcements(request, slug):
	template_name='courses/announcements.html'
	course = get_object_or_404(Course, slug=slug)
	announcements = course.announcements.all()
	if not request.user.is_staff:
		enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

		if not enrollment.is_approved():
			messages.error(request, 'A sua inscrição está pendente')
			return redirect('accounts:dashboard')
	context = {
		'course': course,
		'announcements': announcements
	}
	return render(request, template_name, context)
