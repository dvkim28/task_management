from django import forms

from projects.models import Task


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name',
                  'deadline',
                  'priority',
                  'assigned_to',
                  'task_type',
                  'statuses',
                  'projects']

    def save(self, commit=True, creator=None):
        task = super(CreateTaskForm, self).save(commit=False)
        if creator:
            task.creator = creator
        if commit:
            task.save()
