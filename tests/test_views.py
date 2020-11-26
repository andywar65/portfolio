import os
from datetime import datetime

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from portfolio.models import Project, ProjectStation, StationImage
from users.models import User

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
        ProjectStation.objects.create(prog=prog, title='Station 2')
        noviewer = User.objects.create_user(username='noviewer',
            password='P4s5W0r6')
        viewer = User.objects.create_user(username='viewer',
            password='P4s5W0r6')
        adder = User.objects.create_user(username='adder',
            password='P4s5W0r6')
        content_type = ContentType.objects.get_for_model(ProjectStation)
        permission = Permission.objects.get(
            codename='view_projectstation',
            content_type=content_type,
        )
        viewer.user_permissions.add(permission)
        group = Group.objects.get(name='Project Manager')
        adder.groups.add(group)

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

    def test_station_list_view_status_code_viewer(self):
        self.client.post(reverse('front_login'), {'username':'viewer',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_list',
            kwargs={'slug': 'project'}))
        self.assertEqual(response.status_code, 200)

    def test_station_list_view_status_code_noviewer(self):
        self.client.post(reverse('front_login'), {'username':'noviewer',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_list',
            kwargs={'slug': 'project'}))
        self.assertEqual(response.status_code, 403)

    def test_station_list_view_status_code_wrong_slug(self):
        self.client.post(reverse('front_login'), {'username':'viewer',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_list',
            kwargs={'slug': 'foobar'}))
        self.assertEqual(response.status_code, 404)

    def test_station_list_view_template(self):
        self.client.post(reverse('front_login'), {'username':'viewer',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_list',
            kwargs={'slug': 'project'}))
        self.assertTemplateUsed(response, 'portfolio/projectstation_list.html')

    def test_station_list_view_context(self):
        self.client.post(reverse('front_login'), {'username':'viewer',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_list',
            kwargs={'slug': 'project'}))
        prog = Project.objects.get(slug='project')
        stats = ProjectStation.objects.filter(prog__slug='project')
        self.assertQuerysetEqual(response.context['stations'], stats,
            transform=lambda x: x)
        self.assertEqual(response.context['prog'], prog)

    def test_station_detail_view_status_code_viewer(self):
        self.client.post(reverse('front_login'), {'username':'viewer',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_detail',
            kwargs={'prog_slug': 'project', 'stat_slug': 'station'}))
        self.assertEqual(response.status_code, 200)

    def test_station_detail_view_status_code_noviewer(self):
        self.client.post(reverse('front_login'), {'username':'noviewer',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_detail',
            kwargs={'prog_slug': 'project', 'stat_slug': 'station'}))
        self.assertEqual(response.status_code, 403)

    def test_station_detail_view_status_code_wrong_slug(self):
        self.client.post(reverse('front_login'), {'username':'viewer',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_detail',
            kwargs={'prog_slug': 'project-09-05-20', 'stat_slug': 'station'}))
        self.assertEqual(response.status_code, 404)

    def test_station_detail_view_template(self):
        self.client.post(reverse('front_login'), {'username':'viewer',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_detail',
            kwargs={'prog_slug': 'project', 'stat_slug': 'station'}))
        self.assertTemplateUsed(response, 'portfolio/projectstation_detail.html')

    def test_station_detail_view_context(self):
        self.client.post(reverse('front_login'), {'username':'viewer',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_detail',
            kwargs={'prog_slug': 'project', 'stat_slug': 'station'}))
        stat = ProjectStation.objects.get(slug='station')
        self.assertEqual(response.context['stat'], stat)

    def test_station_create_view_status_code_no_perm(self):
        self.client.post(reverse('front_login'), {'username':'viewer',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_create',
            kwargs={'slug': 'project'}))
        self.assertEqual(response.status_code, 403)

    def test_station_create_view_status_code(self):
        self.client.post(reverse('front_login'), {'username':'adder',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_create',
            kwargs={'slug': 'project'}))
        self.assertEqual(response.status_code, 200)

    def test_station_create_view_template(self):
        self.client.post(reverse('front_login'), {'username':'adder',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_create',
            kwargs={'slug': 'project'}))
        self.assertTemplateUsed(response, 'portfolio/projectstation_form.html')

    def test_station_create_view_template_wrong_slug(self):
        self.client.post(reverse('front_login'), {'username':'adder',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:station_create',
            kwargs={'slug': 'foobar'}))
        self.assertEqual(response.status_code, 404)

    def test_station_create_view_post_success_redirect(self):
        self.client.post(reverse('front_login'), {'username':'adder',
            'password':'P4s5W0r6'})
        prog = Project.objects.get(slug='project')
        response = self.client.post(reverse('portfolio:station_create',
            kwargs={'slug': 'project'}), {'prog': prog.id,
            'title': 'New Station', 'intro': 'Foo'}, follow = True)
        self.assertRedirects(response,
            reverse('portfolio:station_list', kwargs={'slug': 'project'}),
            status_code=302,
            target_status_code = 200)#302 is first step of redirect chain

    def test_station_create_view_post_success_add_another(self):
        self.client.post(reverse('front_login'), {'username':'adder',
            'password':'P4s5W0r6'})
        prog = Project.objects.get(slug='project')
        response = self.client.post(reverse('portfolio:station_create',
            kwargs={'slug': 'project'}), {'prog': prog.id,
            'title': 'New Station', 'intro': 'Foo', 'add_another': ''},
            follow = True)
        self.assertRedirects(response,
            reverse('portfolio:station_create', kwargs={'slug': 'project'}),
            status_code=302,
            target_status_code = 200)#302 is first step of redirect chain

    def test_stationimage_day_archive_view_status_code_no_perm(self):
        self.client.post(reverse('front_login'), {'username':'viewer',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:image_day',
            kwargs={'slug': 'project', 'year': 2020, 'month': 5,
            'day': 9}))
        self.assertEqual(response.status_code, 403)

    def test_stationimage_day_archive_view_status_code(self):
        self.client.post(reverse('front_login'), {'username':'adder',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:image_day',
            kwargs={'slug': 'project', 'year': 2020, 'month': 5,
            'day': 9}))
        self.assertEqual(response.status_code, 200)

    def test_stationimage_day_archive_view_template(self):
        self.client.post(reverse('front_login'), {'username':'adder',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:image_day',
            kwargs={'slug': 'project', 'year': 2020, 'month': 5,
            'day': 9}))
        self.assertTemplateUsed(response,
            'portfolio/stationimage_archive_day.html')

    def test_stationimage_day_archive_view_context(self):
        self.client.post(reverse('front_login'), {'username':'adder',
            'password':'P4s5W0r6'})
        prog = Project.objects.get(slug='project')
        response = self.client.get(reverse('portfolio:image_day',
            kwargs={'slug': 'project', 'year': 2020, 'month': 5,
            'day': 9}))
        self.assertEqual(response.context['prog'], prog)

    def test_stationimage_create_view_status_code_no_perm(self):
        self.client.post(reverse('front_login'), {'username':'viewer',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:image_add',
            kwargs={'prog_slug': 'project', 'stat_slug': 'station' }))
        self.assertEqual(response.status_code, 403)

    def test_stationimage_create_view_status_code(self):
        self.client.post(reverse('front_login'), {'username':'adder',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:image_add',
            kwargs={'prog_slug': 'project', 'stat_slug': 'station' }))
        self.assertEqual(response.status_code, 200)

    def test_stationimage_create_view_status_code_wrong_station(self):
        self.client.post(reverse('front_login'), {'username':'adder',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('portfolio:image_add',
            kwargs={'prog_slug': 'project-09-05-20', 'stat_slug': 'station' }))
        self.assertEqual(response.status_code, 404)
