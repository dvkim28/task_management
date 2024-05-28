from django.views import generic
from django.views.generic import TemplateView

from projects.models import Project


class IndexView(TemplateView):
    template_name = 'pages/index.html'
