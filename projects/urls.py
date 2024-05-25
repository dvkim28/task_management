from django.urls import path

from projects.views import ProjectDetailView, TaskCreateView

app_name = 'projects'

urlpatterns = [
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/create', TaskCreateView.as_view(), name='task_create'),
]
