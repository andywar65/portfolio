from django import forms
from django.forms import ModelForm

from .models import ProjectStation, StationImage

class ProjectStationCreateForm(ModelForm):

    class Meta:
        model = ProjectStation
        fields = '__all__'

class StationImageCreateForm(ModelForm):
    fb_image = forms.ImageField(label='Immagine')

    class Meta:
        model = StationImage
        fields = '__all__'
