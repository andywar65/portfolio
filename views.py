from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Project, ProjectImage

class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'prog'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = ProjectImage.objects.filter(prog_id=self.object.id)
        context['images'] = images
        #if images:
            #context['first_image'] = images[0]
            #context['other_images'] = images[1:]

        return context
