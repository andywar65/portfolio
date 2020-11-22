from django.test import TestCase

from portfolio.models import Project, ProjectStation, StationImage

class ProjectModelTest(TestCase):
    """Testing all methods that don't need SimpleUploadedFile"""
    @classmethod
    def setUpTestData(cls):
        Project.objects.create(title='Project', intro = 'Foo',
            body = 'Bar', site = 'Somewhere', category = 'ALT',
            type = 'ALT', status = 'ALT', cost = 'ALT', )

    def test_project_str_method(self):
        prog = Project.objects.get(slug='project')
        self.assertEquals(prog.__str__(), 'Project')
