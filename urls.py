from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (ProjectListView, ProjectYearArchiveView,
    ProjectCategoryListView, ProjectDetailView, ProjectStationListView,
    ProjectStationDetailView, ProjectStationCreateView,
    StationImageDayArchiveView, StationImageCreateView, ProjectMapDxfCreateView)

app_name = 'portfolio'
urlpatterns = [
    path('', ProjectListView.as_view(), name = 'project_list'),
    path('<int:year>/', ProjectYearArchiveView.as_view(), name = 'year'),
    path(_('category/'), ProjectCategoryListView.as_view(),
        name = 'project_category'),
    path('<slug>/', ProjectDetailView.as_view(), name = 'project_detail'),
    path(_('<slug>/stations/'), ProjectStationListView.as_view(),
        name = 'station_list'),
    path(_('<slug>/stations/add/'), ProjectStationCreateView.as_view(),
        name = 'station_create'),
    path(_('<slug>/stations/dxf/'), ProjectMapDxfCreateView.as_view(),
        name = 'dxf_create'),
    path(_('<slug:prog_slug>/stations/<slug:stat_slug>/'),
        ProjectStationDetailView.as_view(), name = 'station_detail'),
    path(_('<slug:prog_slug>/stations/<slug:stat_slug>/add/'),
        StationImageCreateView.as_view(), name = 'image_add'),
    path(_('<slug>/stations/<int:year>/<int:month>/<int:day>/'),
        StationImageDayArchiveView.as_view(), name = 'image_day'),
    ]
