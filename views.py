from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.dates import YearArchiveView, DayArchiveView
from django.utils.crypto import get_random_string
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import Project, ProjectStation, StationImage, ProjectMapDxf
from .forms import ( ProjectStationCreateForm, StationImageCreateForm,
    ProjectMapDxfCreateForm)
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
            context['cat_filter'] = _('in Category: %(read)s') % {'read': readable}
        elif 'type' in self.request.GET:
            readable = self.get_readable(TYPE, self.request.GET["type"])
            context['cat_filter'] = _('with Intervention type: %(read)s') % {'read': readable}
        elif 'status' in self.request.GET:
            readable = self.get_readable(STATUS, self.request.GET["status"])
            context['cat_filter'] = _('with Status: %(read)s') % {'read': readable}
        elif 'cost' in self.request.GET:
            readable = self.get_readable(COST, self.request.GET["cost"])
            context['cat_filter'] = _('with Cost: %(read)s') % {'read': readable}
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

class ProjectStationListView( PermissionRequiredMixin, ListView):
    model = ProjectStation
    permission_required = 'portfolio.view_projectstation'
    context_object_name = 'stations'
    paginate_by = 12

    def setup(self, request, *args, **kwargs):
        super(ProjectStationListView, self).setup(request, *args, **kwargs)
        self.prog = get_object_or_404( Project, slug = self.kwargs['slug'] )

    def get_queryset(self):
        qs = super(ProjectStationListView, self).get_queryset()
        return qs.filter( prog = self.prog )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prog'] = self.prog
        stat_list = context['stations'].values_list('id')
        context['dates'] = StationImage.objects.filter(stat_id__in=stat_list).dates('date', 'day')
        context['mapbox_token'] = settings.MAPBOX_TOKEN
        return context

class ProjectStationDetailView( PermissionRequiredMixin, DetailView):
    model = ProjectStation
    permission_required = 'portfolio.view_projectstation'
    context_object_name = 'stat'
    slug_field = 'slug'
    slug_url_kwarg = 'stat_slug'

    def get_object(self, queryset=None):
        obj = super(ProjectStationDetailView, self).get_object(queryset=None)
        prog = get_object_or_404( Project, slug = self.kwargs['prog_slug'] )
        if not prog == obj.prog:
            raise Http404(_("Station does not belong to Project"))
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #we add the following to feed the gallery
        context['main_gal_slug'] = get_random_string(7)
        #gallery images
        context['images'] = self.object.station_image.all()

        return context

class ProjectStationCreateView( PermissionRequiredMixin, CreateView ):
    model = ProjectStation
    permission_required = 'portfolio.add_projectstation'
    form_class = ProjectStationCreateForm

    def setup(self, request, *args, **kwargs):
        super(ProjectStationCreateView, self).setup(request, *args, **kwargs)
        #here we get the project by the slug
        self.prog = get_object_or_404( Project, slug = self.kwargs['slug'] )

    def get_initial(self):
        initial = super( ProjectStationCreateView, self ).get_initial()
        initial['prog'] = self.prog.id
        initial['lat'] = self.prog.lat
        initial['long'] = self.prog.long
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #we add the following to feed the map
        context['prog'] = self.prog
        context['mapbox_token'] = settings.MAPBOX_TOKEN

        return context

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return reverse('portfolio:station_create' ,
                kwargs={'slug': self.prog.slug})
        else:
            return reverse('portfolio:station_list' ,
                kwargs={'slug': self.prog.slug})

class ProjectMapDxfCreateView( PermissionRequiredMixin, CreateView ):
    model = ProjectMapDxf
    permission_required = 'portfolio.add_projectmapdxf'
    form_class = ProjectMapDxfCreateForm

    def setup(self, request, *args, **kwargs):
        super(ProjectMapDxfCreateView, self).setup(request, *args, **kwargs)
        #here we get the project by the slug
        self.prog = get_object_or_404( Project, slug = self.kwargs['slug'] )

    def get_initial(self):
        initial = super( ProjectMapDxfCreateView, self ).get_initial()
        initial['prog'] = self.prog.id
        return initial

    def get_success_url(self):
        return reverse('portfolio:station_list' ,
            kwargs={'slug': self.prog.slug})

class StationImageDayArchiveView( PermissionRequiredMixin, DayArchiveView ):
    model = StationImage
    permission_required = 'portfolio.view_stationimage'
    date_field = 'date'
    allow_future = True
    context_object_name = 'images'
    year_format = '%Y'
    month_format = '%m'
    day_format = '%d'
    allow_empty = True

    def setup(self, request, *args, **kwargs):
        super(StationImageDayArchiveView, self).setup(request, *args, **kwargs)
        #here we get the project by the slug
        self.prog = get_object_or_404( Project, slug = self.kwargs['slug'] )

    def get_queryset(self):
        qs = super(StationImageDayArchiveView, self).get_queryset()
        #here we get the station ids by project related name
        stations = self.prog.project_station.values_list('id', flat = True)
        return qs.filter( stat__in = stations )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #we add the following to feed the gallery
        context['main_gal_slug'] = get_random_string(7)
        context['prog'] = self.prog
        return context

class StationImageCreateView( PermissionRequiredMixin, CreateView ):
    model = StationImage
    permission_required = 'portfolio.add_stationimage'
    form_class = StationImageCreateForm

    def setup(self, request, *args, **kwargs):
        super(StationImageCreateView, self).setup(request, *args, **kwargs)
        #here we get the project by the slug
        self.prog = get_object_or_404( Project, slug = self.kwargs['prog_slug'] )
        self.stat = get_object_or_404( ProjectStation, slug = self.kwargs['stat_slug'] )
        if not self.stat.prog == self.prog:
            raise Http404(_("Station does not belong to Project"))

    def get_initial(self):
        initial = super( StationImageCreateView, self ).get_initial()
        initial['stat'] = self.stat.id
        return initial

    def get_success_url(self):
        if 'add_another' in self.request.POST:
            return reverse('portfolio:image_add',
                kwargs={'prog_slug': self.prog.slug,
                'stat_slug': self.stat.slug})
            #return f'/progetti/{ self.prog.slug }/stazioni/{ self.stat.slug }/add'
        else:
            return reverse('portfolio:station_detail',
                kwargs={'prog_slug': self.prog.slug,
                'stat_slug': self.stat.slug})
            #return f'/progetti/{ self.prog.slug }/stazioni/{ self.stat.slug }/'
