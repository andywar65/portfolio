from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (ProjectListView, ProjectYearArchiveView,
    ProjectCategoryListView, ProjectDetailView, )

app_name = 'portfolio'
urlpatterns = [
    path('', ProjectListView.as_view(), name = 'project_list'),
    path('<int:year>/', ProjectYearArchiveView.as_view(), name = 'year'),
    path(_('category/'), ProjectCategoryListView.as_view(),
        name = 'project_category'),
    path('<slug>/', ProjectDetailView.as_view(), name = 'project_detail'),
    ]
