from django.conf import settings
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.dates import YearArchiveView
from django.utils.crypto import get_random_string

from imap_tools import MailBox, AND

from .models import Project, ProjectStation
from pages.models import GalleryImage
from .management.commands.fetch_portfolio_emails import do_command
from .choices import *

class ProjectListView(ListView):
    model = Project
    context_object_name = 'progs'
    paginate_by = 12

    def setup(self, request, *args, **kwargs):
        super(ProjectListView, self).setup(request, *args, **kwargs)
        do_command()

class ProjectYearArchiveView(YearArchiveView):
    model = Project
    make_object_list = True
    date_field = 'date'
    allow_future = True
    context_object_name = 'progs'
    year_format = '%Y'
    allow_empty = True

class ProjectCategoryListView(ListView):
    model = Project
    context_object_name = 'progs'
    template_name = 'portfolio/project_category_list.html'
    paginate_by = 12
    allow_empty = False

    def get_readable(self, list, target):
        for i in list:
            if i[0] == target:
                return i[1]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'category' in self.request.GET:
            readable = self.get_readable(CATEGORY, self.request.GET["category"])
            context['cat_filter'] = f'in Categoria: {readable}'
        elif 'type' in self.request.GET:
            readable = self.get_readable(TYPE, self.request.GET["type"])
            context['cat_filter'] = f'di Intervento: {readable}'
        elif 'status' in self.request.GET:
            readable = self.get_readable(STATUS, self.request.GET["status"])
            context['cat_filter'] = f'con Status: {readable}'
        elif 'cost' in self.request.GET:
            readable = self.get_readable(COST, self.request.GET["cost"])
            context['cat_filter'] = f'di Costo: {readable}'
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if 'category' in self.request.GET:
            qs = qs.filter(category=self.request.GET['category'])
        elif 'type' in self.request.GET:
            qs = qs.filter(type=self.request.GET['type'])
        elif 'status' in self.request.GET:
            qs = qs.filter(status=self.request.GET['status'])
        elif 'cost' in self.request.GET:
            qs = qs.filter(cost=self.request.GET['cost'])
        return qs

class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'prog'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #we add the following to feed standardized gallery
        context['main_gal_slug'] = get_random_string(7)
        context['title'] = self.object.title
        #gallery images
        context['images'] = self.object.project_image.all()

        return context

class ProjectStationListView(ListView):
    model = ProjectStation
    context_object_name = 'stations'
    paginate_by = 12
