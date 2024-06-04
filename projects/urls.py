from django.urls import path

from projects.views import (ProjectCreateView,
                            ProjectDetailView,
                            TaskCreateView,
                            TaskDetailView,
                            TasksListView,
                            ProjectUpdateView)

app_name = 'projects'

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/admin/', ProjectUpdateView.as_view(), name='project_admin'),
    path('create-task/', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('my-task/', TasksListView.as_view(), name='task-list'),
]
