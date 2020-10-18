from django.urls import path

from .views import ProjectDetailView

app_name = 'portfolio'
urlpatterns = [
    path('<slug>/', ProjectDetailView.as_view(), name = 'project_detail'),
    ]
