from django.contrib import admin

from projects.models import Comment, Project, Task, TaskType


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'creator',
                    'projects',
                    'assigned_to',
                    'deadline',
                    'statuses')
    list_filter = ('projects',)
    search_fields = ('title',
                     'creator__username',
                     'assigned_to__username')


admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(TaskType)
