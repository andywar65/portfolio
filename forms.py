from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from .models import Project, ProjectStation, StationImage

class ProjectStationCreateForm(ModelForm):
    prog = forms.ModelChoiceField( label=_('Project'),
        queryset=Project.objects.all(), disabled = True )

    class Meta:
        model = ProjectStation
        fields = '__all__'

class StationImageCreateForm(ModelForm):
    image = forms.ImageField(label=_('Image'), required=True)

    class Meta:
        model = StationImage
        fields = ( 'stat', 'date', 'image', 'caption')
