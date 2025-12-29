from django.shortcuts import render, get_object_or_404
from .models import Project

def project_list(request):
    projects = Project.objects.order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/project_detail.html', {'project': project})