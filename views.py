from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Project, ProjectImage

class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'

class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'prog'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = ProjectImage.objects.filter(prog_id=self.object.id)
        context['images'] = images

        return context
