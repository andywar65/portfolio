from django.urls import path

from .views import ProjectListView, ProjectDetailView

app_name = 'portfolio'
urlpatterns = [
    path('', ProjectListView.as_view(), name = 'project_list'),
    path('<slug>/', ProjectDetailView.as_view(), name = 'project_detail'),
    ]
