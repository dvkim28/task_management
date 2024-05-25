from django.views.generic import TemplateView

from projects.models import Project


class IndexView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(crew=self.request.user)
        return context
