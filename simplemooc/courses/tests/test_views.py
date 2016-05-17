from django.test import TestCase
from django.core import mail
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from simplemooc.courses.models import Course

class HomeViewTest(TestCase):

	def test_home_code(self):
		client = Client()
		response = client.get(reverse('core:home'))
		self.assertEqual(response.status_code, 200)

	def test_home_template_used(self):
		client = Client()
		response = client.get(reverse('core:home'))
		self.assertTemplateUsed(response, 'home.html')
		self.assertTemplateUsed(response, 'base.html')

class ContactCourseTestCase(TestCase):

	def setUp(self):
		self.course = Course.objects.create(name='Django', slug='django')

	def tearDown(self):

		self.course.delete()

	def test_contact_form_error(self):

		data = {'name': 'Fulano', 'email': '', 'message': ''}
		client = Client()
		path = reverse('courses:details', args=[self.course.slug])
		response = client.post(path, data)
		self.assertFormError(response, 'form', 'email', 'Este campo e obrigatorio')
		self.assertFormError(response, 'form', 'message', 'Este campo e obrigatorio')

	def test_contact_form_sucess(self):

		data = {'name': 'Fulano', 'email': 'nrdesales@hotmail.com', 'message': 'Oi'}
		client = Client()
		path = reverse('courses:details', args=[self.course.slug])
		response = client.post(path, data)
		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])