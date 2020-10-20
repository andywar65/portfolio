from django.conf import settings
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from imap_tools import MailBox, AND

from .models import Project, ProjectImage
from pages.models import GalleryImage
from .management.commands.fetch_portfolio_emails import do_command

class ProjectListView(ListView):
    model = Project
    context_object_name = 'progs'
    paginate_by = 12

    def setup(self, request, *args, **kwargs):
        super(ProjectListView, self).setup(request, *args, **kwargs)
        do_command()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """Using standard Gallery from Pages module. To avoid circular import
        we construct a dictionary of projects with their first image"""
        context['prog_image'] = {}
        for prog in context['progs']:
            image = GalleryImage.objects.filter(prog_id=prog.id).first()
            context['prog_image'][prog] = image
        return context

class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'prog'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #we add the following to feed standardized gallery
        #TODO this can work if images are file browser fields
        context['uuid'] = self.object.id
        context['title'] = self.object.title
        #gallery images
        images = GalleryImage.objects.filter(prog_id=self.object.id)
        context['images'] = images

        return context
