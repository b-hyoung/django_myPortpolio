from .models import Post
from projects.models import Project

def recent_posts(request):
    recent_posts = Post.objects.order_by('-created_at')[:5]
    return {'recent_posts': recent_posts}

def sidebar_projects(request):
    projects = Project.objects.filter(is_visible=True).order_by('-created_at')[:4]
    
    project_data = []
    for project in projects:
        techs = [tech.strip() for tech in project.technologies.split(',') if tech.strip()]
        
        project_data.append({
            'id': project.id,
            'title': project.title,
            'skills': techs[:3],
            'more_skills': len(techs) > 3,
        })
        
    return {'sidebar_projects': project_data}


def default_template_variables(request):
    return {
        'show_hero_section': True,
    }
