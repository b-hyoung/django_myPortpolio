from .models import Post
from projects.models import Project

def recent_posts(request):
    recent_posts = Post.objects.order_by('-created_at')[:5]
    return {'recent_posts': recent_posts}

def sidebar_projects(request):
    # Skill to color mapping based on the image
    skill_color_map = {
        'Python': 'teal', 'Java': 'teal', 'JavaScript': 'teal',
        'NextJs': 'purple', 'Spring Boot': 'purple', 'React': 'purple', 'Django': 'purple',
        'Docker': 'teal', 'Git & GitHub': 'teal', 'PostgreSQL': 'teal', 'AWS': 'teal',
        'MySQL': 'purple', 'MongoDB': 'purple',
        'Docker Compose': 'teal', 'Kubernetes': 'teal',
    }

    projects = Project.objects.filter(is_visible=True).order_by('-created_at')[:4]
    
    project_data = []
    for project in projects:
        techs_raw_from_comma = [tech.strip() for tech in project.technologies.split(',') if tech.strip()]
        
        techs_final = []
        for tech_chunk in techs_raw_from_comma:
            techs_final.extend([t.strip() for t in tech_chunk.split(' ') if t.strip()])

        # Prepare skill objects with name and color
        skills_with_colors = []
        for tech in techs_final:
            skill_color = skill_color_map.get(tech, 'teal') # Default to teal if not in map
            skills_with_colors.append({'name': tech, 'color': skill_color})

        project_data.append({
            'id': project.id,
            'title': project.title,
            'skills': skills_with_colors[:3], # Still limit to 3 for initial display
            'more_skills': len(skills_with_colors) > 3,
        })
        
    return {'sidebar_projects': project_data}


def default_template_variables(request):
    return {
        'show_hero_section': True,
    }
