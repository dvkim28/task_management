from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.generic import TemplateView

from logs.models import Log
from projects.models import Task


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["expired_tasks"] = self.get_expired_tasks()
        context["percent_of_expired_tasks"] = (
            self.get_percent_of_expired_tasks())
        context["bugs"] = self.get_bugs()
        context["percent_of_bugs"] = self.get_percent_of_bugs()
        logs, page_obj = self.get_logs()
        context["logs"] = logs
        context["page_obj"] = page_obj
        return context

    def get_user_tasks(self):
        return Task.objects.filter(
            assigned_to=self.request.user,
            is_done=False)

    def get_expired_tasks(self):
        tasks = self.get_user_tasks()
        time = timezone.now()
        expired_tasks = tasks.filter(deadline__lte=time, is_done=False)
        return expired_tasks

    def get_percent_of_expired_tasks(self):
        tasks = self.get_user_tasks()
        expired_tasks = self.get_expired_tasks()
        if tasks.count() == 0:
            return 0
        return round((expired_tasks.count() / tasks.count()) * 100,)

    def get_percent_of_bugs(self):
        tasks = self.get_user_tasks()
        bugs = self.get_bugs()
        if tasks.count() == 0:
            return 0
        return round((bugs.count() / tasks.count()) * 100,)

    def get_bugs(self):
        tasks = self.get_user_tasks()
        bugs = tasks.filter(task_type__name="Bug")
        return bugs

    def get_logs(self):
        projects = list(self.request.user.projects.all())
        all_logs = []
        for project in projects:
            logs = Log.objects.filter(project=project)
            all_logs.extend(logs)
        paginator = Paginator(all_logs, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj.object_list, page_obj
