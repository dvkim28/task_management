from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from accounts.models import User
from projects.forms import CreateTaskForm, CommentForm, TaskGeneralForm, InviteNewMemberForm
from projects.models import Project, Task


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ["name", "description"]
    template_name = "pages/project-create.html"

    def post(self, request, *args, **kwargs):
        manager = request.user
        form = self.get_form()
        if form.is_valid():
            form.save()
            form.instance.managements.add(manager)
            manager.projects.add(form.instance)
            project_pk = form.instance.pk
            return HttpResponseRedirect(
                reverse_lazy("projects:project_detail",
                             kwargs={"pk": project_pk}))

    def get_success_url(self):
        return reverse_lazy("projects:project_detail", kwargs={
            "pk": self.object.id})


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "pages/project_view.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context["InviteNewMemberForm"] = InviteNewMemberForm
        context["members"] = User.objects.filter(projects=self.object)
        context["percent_of_task"] = (Task.objects.all())
        return context

    def post(self, request, *args, **kwargs):
        form = InviteNewMemberForm(request.POST)
        if form.is_valid():
            project = self.get_object()
            users = form.cleaned_data['projects']
            for user in users:
                user_obj = User.objects.get(pk=user.pk)
                user_obj.projects.add(project)
            return HttpResponseRedirect(
                reverse_lazy("projects:project_detail", kwargs={"pk": project.pk})
            )
        return self.get(request, *args, **kwargs)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "pages/task_form.html"
    form_class = CreateTaskForm

    def get_success_url(self):
        return reverse_lazy(
            "projects:project_detail", kwargs={
                "pk": self.object.projects.pk
            }
        )

    def post(self, request, *args, **kwargs):
        form = CreateTaskForm(request.POST)
        creator = request.user
        if form.is_valid():
            form.instance.creator = creator
            form.save()
            project_pk = form.instance.projects.pk
            return HttpResponseRedirect(
                reverse_lazy("projects:project_detail",
                             kwargs={"pk": project_pk}))


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "pages/task-detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context["CommentForm"] = CommentForm()
        context["TaskGeneralForm"] = TaskGeneralForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        author = request.user
        project = Project.objects.get(pk=self.object.projects.pk)

        if form.is_valid():
            form.instance.projects = project
            form.instance.author = author
            form.instance.task = self.object
            form.save()
            task_pk = form.instance.task.pk
            return HttpResponseRedirect(
                reverse_lazy("projects:task_detail", kwargs={"pk": task_pk})
            )
        else:
            form = TaskGeneralForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                deadline = data.get("deadline")
                task_pk = self.object.pk
                task = self.object
                task.priority = data.get("priority")
                task.assigned_to = data.get("assigned_to")
                task.deadline = deadline
                task.status = data.get("status")
                task.save()
            return HttpResponseRedirect(
                reverse_lazy("projects:task_detail", kwargs={"pk": task_pk})
            )
