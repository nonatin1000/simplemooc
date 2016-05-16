# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Announcement, Lesson, Material
from .forms import ContactCourse, CommentForm
from .decorators import enrollment_required

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
		messages.success(request, 'Você foi inscrito no curso com sucesso')
	else:
		messages.info(request, 'Você já está inscrito no curso')

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
@enrollment_required
def announcements(request, slug):
	course = request.course
	template_name='courses/announcements.html'
	announcements = course.announcements.all()
	context = {
		'course': course,
		'announcements': announcements
	}
	return render(request, template_name, context)

@login_required
@enrollment_required
def show_announcement(request, slug, pk):
	course = request.course
	announcement = get_object_or_404(course.announcements.all(), pk=pk)
	form = CommentForm(request.POST or None)
	if form.is_valid():
		comment = form.save(commit=False)
		comment.user = request.user
		comment.announcement = announcement
		comment.save()
		form = CommentForm()
		messages.add_message(request, messages.SUCCESS, 'Seu comentário foi enviado com sucesso.')
	
	template_name='courses/show_announcement.html'
	
	context = {
		'course': course,
		'announcement': announcement,
		'form': form
	}
	return render(request, template_name, context)

@login_required
@enrollment_required
def lessons(request, slug):
	course = request.course
	template_name = 'courses/lessons.html'
	lessons = course.release_lessons()
	if request.user.is_staff:
		lessons = course.lessons.all()
	context = {
		'course': course,
		'lessons': lessons
	}
	return render(request, template_name, context)

@login_required
@enrollment_required
def lesson(request, slug, pk):
	course = request.course
	lesson = get_object_or_404(Lesson, pk=pk, course=course)
	if not request.user.is_staff and not lesson.is_available():
		messages.error(request, 'Esta aula não está disponível')
		return redirect('courses:lessons', slug=course.slug)
	template_name = 'courses/lesson.html'
	context = {
		'course': course,
		'lesson': lesson,
	}
	return render(request, template_name, context)

@login_required
@enrollment_required
def material(request, slug, pk):
	course = request.course
	material = get_object_or_404(Material, pk=pk, lesson__course=course)
	lesson = material.lesson
	if not request.user.is_staff and not lesson.is_available():
		messages.error(request, 'Este material não está disponível')
		return redirect('courses:lesson', slug=course.slug, pk=lesson.pk)
	if not material.is_embedded():
		return redirect(material.file.url)
	template_name = 'courses/material.html'
	context = {
		'course': course,
		'lesson': lesson,
		'material': material,
	}
	return render(request, template_name, context)