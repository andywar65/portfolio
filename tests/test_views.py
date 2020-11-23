import os
from datetime import datetime

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from portfolio.models import Project, ProjectStation, StationImage

@override_settings(USE_I18N=False)
class ProjectViewsTest(TestCase):
    """Testing all methods that don't need SimpleUploadedFile"""
    @classmethod
    def setUpTestData(cls):
        prog = Project.objects.create(title='Project', intro = 'Foo',
            body = 'Bar', site = 'Somewhere', category = 'ALT',
            type = 'ALT', status = 'ALT', cost = 'ALT', )
        Project.objects.create(date=datetime.strptime('2020-05-09', '%Y-%m-%d'))
        stat = ProjectStation.objects.create(prog=prog, title='Station')

    def test_project_list_view_status_code(self):
        response = self.client.get(reverse('portfolio:project_list'))
        self.assertEqual(response.status_code, 200)

    def test_project_list_view_template(self):
        response = self.client.get(reverse('portfolio:project_list'))
        self.assertTemplateUsed(response, 'portfolio/project_list.html')

    def test_project_list_view_context(self):
        response = self.client.get(reverse('portfolio:project_list'))
        progs = Project.objects.all()
        self.assertQuerysetEqual(response.context['progs'], progs,
            transform=lambda x: x)
