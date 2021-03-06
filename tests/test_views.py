import os
from datetime import datetime

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from imap_tools.message import MailMessage

from portfolio.models import Project
from portfolio.management.commands.fetch_portfolio_emails import process_message
from users.models import User
from pages.models import GalleryImage

@override_settings(USE_I18N=False)
@override_settings(MEDIA_ROOT=os.path.join(settings.MEDIA_ROOT, 'temp'))
class ProjectViewsTest(TestCase):
    """Testing all methods that don't need SimpleUploadedFile"""
    @classmethod
    def setUpTestData(cls):
        prog = Project.objects.create(title='Project', intro = 'Foo',
            body = 'Bar', site = 'Somewhere', category = 'ALT',
            type = 'ALT', status = 'ALT', cost = 'ALT', )
        Project.objects.create(date=datetime.strptime('2020-05-09', '%Y-%m-%d'))
        #stat = ProjectStation.objects.create(prog=prog, title='Station')
        #ProjectStation.objects.create(prog=prog, title='Station 2')
        noviewer = User.objects.create_user(username='noviewer',
            password='P4s5W0r6')
        viewer = User.objects.create_user(username='viewer',
            password='P4s5W0r6')
        adder = User.objects.create_user(username='adder',
            password='P4s5W0r6')
        #content_type = ContentType.objects.get_for_model(ProjectStation)
        #permission = Permission.objects.get(
            #codename='view_projectstation',
            #content_type=content_type,
        #)
        #viewer.user_permissions.add(permission)
        group = Group.objects.get(name='Project Manager')
        adder.groups.add(group)

    def tearDown(self):
        """Checks existing files, then removes them"""
        try:
            list = os.listdir(os.path.join(settings.MEDIA_ROOT,
                'uploads/images/galleries/'))
        except:
            return
        for file in list:
            os.remove(os.path.join(settings.MEDIA_ROOT,
                f'uploads/images/galleries/{file}'))

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

    def test_project_category_list_view_status_code(self):
        response = self.client.get(reverse('portfolio:project_category')+
            '?category=ALT')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('portfolio:project_category')+
            '?type=ALT')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('portfolio:project_category')+
            '?status=ALT')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('portfolio:project_category')+
            '?cost=ALT')
        self.assertEqual(response.status_code, 200)

    def test_project_category_list_view_template(self):
        response = self.client.get(reverse('portfolio:project_category')+
            '?category=ALT')
        self.assertTemplateUsed(response, 'portfolio/project_category_list.html')
        response = self.client.get(reverse('portfolio:project_category')+
            '?type=ALT')
        self.assertTemplateUsed(response, 'portfolio/project_category_list.html')
        response = self.client.get(reverse('portfolio:project_category')+
            '?status=ALT')
        self.assertTemplateUsed(response, 'portfolio/project_category_list.html')
        response = self.client.get(reverse('portfolio:project_category')+
            '?cost=ALT')
        self.assertTemplateUsed(response, 'portfolio/project_category_list.html')

    def test_project_category_list_view_context(self):
        response = self.client.get(reverse('portfolio:project_category')+
            '?category=ALT')
        progs = Project.objects.filter(category='ALT')
        self.assertQuerysetEqual(response.context['progs'], progs,
            transform=lambda x: x)
        response = self.client.get(reverse('portfolio:project_category')+
            '?type=ALT')
        progs = Project.objects.filter(type='ALT')
        self.assertQuerysetEqual(response.context['progs'], progs,
            transform=lambda x: x)
        response = self.client.get(reverse('portfolio:project_category')+
            '?status=ALT')
        progs = Project.objects.filter(status='ALT')
        self.assertQuerysetEqual(response.context['progs'], progs,
            transform=lambda x: x)
        response = self.client.get(reverse('portfolio:project_category')+
            '?cost=ALT')
        progs = Project.objects.filter(cost='ALT')
        self.assertQuerysetEqual(response.context['progs'], progs,
            transform=lambda x: x)

    def test_project_detail_view_status_code(self):
        response = self.client.get(reverse('portfolio:project_detail',
            kwargs={'slug': 'project'}))
        self.assertEqual(response.status_code, 200)

    def test_project_detail_view_template(self):
        response = self.client.get(reverse('portfolio:project_detail',
            kwargs={'slug': 'project'}))
        self.assertTemplateUsed(response, 'portfolio/project_detail.html')

    def test_project_detail_view_context(self):
        response = self.client.get(reverse('portfolio:project_detail',
            kwargs={'slug': 'project'}))
        prog = Project.objects.get(slug='project')
        self.assertEqual(response.context['prog'], prog)

    def test_process_message_with_attachment(self):
        manager = User.objects.get(username='adder')
        msg_path = os.path.join(settings.STATIC_ROOT,
            'portfolio/sample/with_att.eml')
        with open(msg_path, 'rb') as f:
            bytes_data = f.read()
        message = MailMessage.from_bytes(bytes_data)
        process_message(message, manager)
        prog = Project.objects.get(slug='email-project')
        self.assertEqual(prog.title, "Email project")
        image = GalleryImage.objects.get(prog_id=prog.id)
        self.assertEqual(image.caption, "Logo")
