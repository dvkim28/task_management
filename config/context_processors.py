from projects.models import Project


def return_projects(request):
    return {"projects": Project.objects.filter(crew=request.user)}