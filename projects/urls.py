from django.urls import include, path

from config.views import index
from projects.views import index_view

app_name = 'projects'

urlpatterns = [
    path('',index_view, name='index'),

]
