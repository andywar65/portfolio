from django.urls import path

from .views import (ProjectListView, ProjectYearArchiveView,
    ProjectCategoryListView, ProjectDetailView, ProjectStationListView,
    ProjectStationDetailView,)

app_name = 'portfolio'
urlpatterns = [
    path('', ProjectListView.as_view(), name = 'project_list'),
    path('<int:year>/', ProjectYearArchiveView.as_view(), name = 'year'),
    path('categoria/', ProjectCategoryListView.as_view(),
        name = 'project_category'),
    path('<slug>/', ProjectDetailView.as_view(), name = 'project_detail'),
    path('<slug>/stazioni/', ProjectStationListView.as_view(),
        name = 'station_list'),
    path('<slug:prog_slug>/stazioni/<slug:stat_slug>/',
        ProjectStationDetailView.as_view(), name = 'station_detail'),
    ]
