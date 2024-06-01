from projects.models import Project


def get_projects(request):
    projects = Project.objects.all()
    return {"projects":projects}