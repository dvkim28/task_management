from django import forms

from projects.models import Task, Comment


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title',
                  'deadline',
                  'priority',
                  'description',
                  'assigned_to',
                  'task_type',
                  'projects']

    def save(self, commit=True, creator=None):
        task = super(CreateTaskForm, self).save(commit=False)
        if creator:
            task.creator = creator
        if commit:
            task.save()


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Add a comment...',
    }),
        label=''
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
