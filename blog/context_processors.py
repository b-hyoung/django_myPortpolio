from .models import Post

def recent_posts(request):
    recent_posts = Post.objects.order_by('-created_at')[:5]
    return {'recent_posts': recent_posts}

def default_template_variables(request):
    return {
        'show_hero_section': True,
    }
