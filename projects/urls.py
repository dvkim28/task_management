from django.urls import path

from projects.views import ProjectDetailView

app_name = 'projects'

urlpatterns = [
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
]
