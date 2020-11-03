from django.forms import ModelForm

from .models import ProjectStation

class ProjectStationCreateForm(ModelForm):

    class Meta:
        model = ProjectStation
        fields = '__all__'
