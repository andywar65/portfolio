from django.conf import settings
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from imap_tools import MailBox, AND

from .models import Project
from pages.models import GalleryImage
from .management.commands.fetch_portfolio_emails import do_command

class ProjectListView(ListView):
    model = Project
    context_object_name = 'progs'
    paginate_by = 12

    def setup(self, request, *args, **kwargs):
        super(ProjectListView, self).setup(request, *args, **kwargs)
        do_command()

class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'prog'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #we add the following to feed standardized gallery
        context['slug'] = self.object.slug
        context['title'] = self.object.title
        #gallery images
        context['images'] = self.object.project_image.all()

        return context
