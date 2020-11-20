from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from .models import ProjectStation, StationImage

class ProjectStationCreateForm(ModelForm):

    class Meta:
        model = ProjectStation
        fields = '__all__'

class StationImageCreateForm(ModelForm):
    image = forms.ImageField(label=_('Image'), required=True)

    class Meta:
        model = StationImage
        fields = ( 'stat', 'date', 'image', 'caption')
