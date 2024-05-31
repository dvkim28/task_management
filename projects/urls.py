from django.urls import path

from projects.views import (ProjectCreateView, ProjectDetailView,
                            TaskCreateView, TaskDetailView, TasksListView)

app_name = 'projects'

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('create-task/', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('my-task/', TasksListView.as_view(), name='task-list'),
]
