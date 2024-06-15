from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.models import User
from logs.models import Log
from projects.forms import (CommentForm,
                            CreateTaskForm,
                            InviteNewMemberForm,
                            TaskGeneralForm,
                            FilterByProjectForm,
                            FilterByMembersForm,
                            ProjectMemberForm,
                            ProjectManagementForm,
                            ProjectManagementInvitationForm, GeneralInfoForm)
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
        context["members"] = User.objects.filter(
            projects=self.object).select_related("projects")
        context["filter_form"] = FilterByMembersForm(
            self.request.GET,
            project=self.object)
        context["tasks"] = self.get_tasks_by_member()
        return context

    def get_tasks_by_member(self):
        tasks = (Task.objects.filter(projects=self.object).
                 select_related("assigned_to", "task_type", "projects"))
        if self.request.method == "GET":
            form = FilterByMembersForm(self.request.GET, project=self.object)
            if form.is_valid():
                member = form.cleaned_data["member"]
                if member is not None:
                    filtered_tasks = tasks.filter(assigned_to=member)
                    return filtered_tasks
        return tasks

    def post(self, request, *args, **kwargs):
        form = InviteNewMemberForm(request.POST)
        if form.is_valid():
            project = self.get_object()
            users = form.cleaned_data['projects']
            for user in users:
                user_obj = User.objects.get(pk=user.pk)
                user_obj.projects.add(project)
            return HttpResponseRedirect(
                reverse_lazy("projects:project_detail",
                             kwargs={"pk": project.pk})
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
            project_pk = form.instance.projects.pk
            form.save()
            project = Project.objects.get(pk=project_pk)
            task = form.instance
            Log.objects.create(
                user=self.request.user,
                action=f"Created task: {task.title}",
                project=project,
            )
            return HttpResponseRedirect(
                reverse_lazy("projects:project_detail",
                             kwargs={"pk": project.pk}))
        return render(request, 'pages/task_form.html', {'form': form})


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "pages/task-detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context["CommentForm"] = CommentForm()
        context["TaskGeneralForm"] = TaskGeneralForm(
            project=self.object.projects,
            instance=self.object,
        )
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
            task = Task.objects.get(pk=form.instance.task.pk)
            Log.objects.create(
                user=self.request.user,
                action=f"Added comment to the task: {task.title}",
                project=project,
            )
            return HttpResponseRedirect(
                reverse_lazy("projects:task_detail", kwargs={"pk": task.pk})
            )
        else:
            form = TaskGeneralForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                deadline = data["deadline"]
                task = self.object
                task.priority = data["priority"]
                task.assigned_to = data["assigned_to"]
                task.deadline = deadline
                task.status = data["status"]
                task.save()
                Log.objects.create(
                    user=self.request.user,
                    action=f"Updated task: {task.title}",
                    project=project,
                )
            return HttpResponseRedirect(
                reverse_lazy("projects:task_detail",
                             kwargs={"pk": self.object.pk})
            )


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "pages/task-list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(TasksListView, self).get_context_data(*kwargs)
        context["FilterByProjectForm"] = FilterByProjectForm()
        return context

    def get_queryset(self):
        tasks = Task.objects.filter(assigned_to=self.request.user)
        filter_form = FilterByProjectForm(self.request.GET)
        if filter_form.is_valid() and filter_form.cleaned_data['projects']:
            return tasks.filter(projects=filter_form.cleaned_data['projects'])
        return tasks


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = "pages/project-admin.html"
    form_class = GeneralInfoForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            self.update_project(form)

        self.handle_member_form(request)
        self.handle_management_form(request)
        self.handle_management_invitation_form(request)
        self.handle_invite_new_member_form(request)

        return HttpResponseRedirect(
            reverse_lazy("projects:project_detail", kwargs={"pk": self.object.pk})
        )

    def update_project(self, form):
        project = self.object
        if form.data.get("name"):
            project.name = form.data.get("name")
        if form.data.get("description"):
            project.description = form.data.get("description")
        project.save()

    def handle_member_form(self, request):
        member_form = ProjectMemberForm(request.POST, project=self.object)
        if member_form.is_valid():
            for member in member_form.cleaned_data['projects']:
                self.remove_member(member)

    def handle_management_form(self, request):
        management_form = ProjectManagementForm(request.POST, project=self.object)
        if management_form.is_valid():
            for member in management_form.cleaned_data['projects']:
                self.remove_management(member)

    def handle_management_invitation_form(self, request):
        management_invitation_form = ProjectManagementInvitationForm(request.POST, project=self.object)
        if management_invitation_form.is_valid():
            for member in management_invitation_form.cleaned_data['member']:
                self.add_management(member)

    def handle_invite_new_member_form(self, request):
        form = InviteNewMemberForm(request.POST)
        if form.is_valid():
            users = form.cleaned_data['projects']
            for user in users:
                self.add_member(user)

    def remove_member(self, member):
        try:
            user = User.objects.get(pk=member.id)
            user.projects.remove(self.object)
            user.save()
        except User.DoesNotExist:
            pass

    def remove_management(self, member):
        try:
            user = User.objects.get(pk=member.id)
            self.object.managements.remove(user)
            self.object.save()
        except User.DoesNotExist:
            pass

    def add_management(self, member):
        try:
            user = User.objects.get(pk=member.id)
            self.object.managements.add(user)
        except User.DoesNotExist:
            pass

    def add_member(self, user):
        try:
            user_obj = User.objects.get(pk=user.pk)
            user_obj.projects.add(self.object)
        except User.DoesNotExist:
            pass

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        context["MemberForm"] = ProjectMemberForm(project=self.object)
        context["ManagementForm"] = ProjectManagementForm(project=self.object)
        context["management_invitation_form"] = ProjectManagementInvitationForm(project=self.object)
        context["InviteNewMemberForm"] = InviteNewMemberForm(project=self.object)
        return context
