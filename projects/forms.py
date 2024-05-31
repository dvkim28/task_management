from django import forms
from django.forms import DateInput

from accounts.models import User
from projects.models import Comment, Task, Project


class CreateTaskForm(forms.ModelForm):
    deadline = forms.DateField(widget=DateInput(attrs={"type": "date"}))

    class Meta:
        model = Task
        fields = ["title",
                  "deadline",
                  "priority",
                  "description",
                  "assigned_to",
                  "task_type",
                  "projects"]

    def save(self, commit=True, creator=None):
        task = super(CreateTaskForm, self).save(commit=False)
        if creator:
            task.creator = creator
        if commit:
            task.save()


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Add a comment...",
    }),
        label=""
    )

    class Meta:
        model = Comment
        fields = ["text"]

    def save(self, commit=True, creator=None):
        comment = super(CommentForm, self).save(commit=False)
        if creator:
            comment.author = creator
        if commit:
            comment.save()


class TaskGeneralForm(forms.ModelForm):
    deadline = forms.DateField(widget=DateInput(attrs={"type": "date"}))

    class Meta:
        model = Task
        fields = ["priority", "assigned_to", "deadline", "status", ]


class InviteNewMemberForm(forms.ModelForm):
    projects = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(),
        label="",
    )

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(InviteNewMemberForm, self).__init__(*args, **kwargs)
        if project:
            project_users = User.objects.filter(projects__id=project.id)
            self.fields['projects'].queryset = User.objects.exclude(id__in=project_users)

    class Meta:
        model = User
        fields = ["projects"]


class FilterByProjectForm(forms.Form):
    projects = forms.ModelChoiceField(
        label="",
        queryset=Project.objects.all(),
        required=False,
        empty_label="Filter by project",
    )
