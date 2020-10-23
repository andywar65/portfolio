from django.urls import path

from .views import ProjectListView, ProjectYearArchiveView, ProjectDetailView

app_name = 'portfolio'
urlpatterns = [
    path('', ProjectListView.as_view(), name = 'project_list'),
    path('<int:year>/', ProjectYearArchiveView.as_view(), name = 'year'),
    path('<slug>/', ProjectDetailView.as_view(), name = 'project_detail'),
    ]
