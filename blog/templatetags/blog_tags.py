from django import template
from django.utils.html import mark_safe, format_html
import markdown
import re

register = template.Library()

@register.filter(name='startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False

@register.filter
def markdownify(text):
    return mark_safe(markdown.markdown(text, extensions=['extra', 'nl2br', 'fenced_code', 'codehilite'], extension_configs={'codehilite': {'css_class': 'highlight', 'noclasses': True}}))

@register.simple_tag
def get_tech_icon(technology_name):
    """
    Maps a technology name to a Devicon icon tag.
    """
    raw_name = (technology_name or "").strip()
    # Normalize common punctuation/format variants: "Python,", "Next.js", "AWS(EC2)"
    normalized_name = re.sub(r'[,\s]+$', '', raw_name)
    normalized_name = re.sub(r'\(.*?\)', '', normalized_name).strip()
    tech_name_lower = normalized_name.lower()
    
    ICON_MAP = {
        'python': 'devicon-python-plain',
        'django': 'devicon-django-plain',
        'javascript': 'devicon-javascript-plain',
        'html': 'devicon-html5-plain',
        'html5': 'devicon-html5-plain',
        'css': 'devicon-css3-plain',
        'css3': 'devicon-css3-plain',
        'bootstrap': 'devicon-bootstrap-plain',
        'react': 'devicon-react-original',
        'zustand': 'devicon-redux-original',
        'vue': 'devicon-vuejs-plain',
        'angular': 'devicon-angularjs-plain',
        'typescript': 'devicon-typescript-plain',
        'docker': 'devicon-docker-plain',
        'postgresql': 'devicon-postgresql-plain',
        'mysql': 'devicon-mysql-plain',
        'sqlite': 'devicon-sqlite-plain',
        'git': 'devicon-git-plain',
        'github': 'devicon-github-original',
        'gitlab': 'devicon-gitlab-plain',
        'nginx': 'devicon-nginx-original',
        'linux': 'devicon-linux-plain',
        'ubuntu': 'devicon-ubuntu-plain',
        'figma': 'devicon-figma-plain',
        'svelte': 'devicon-svelte-plain',
        'fastapi': 'devicon-fastapi-plain',
        'firebase': 'devicon-firebase-plain',
        'graphql': 'devicon-graphql-plain',
        'redis': 'devicon-redis-plain',
        'mongodb': 'devicon-mongodb-plain',
        'nodejs': 'devicon-nodejs-plain',
        'npm': 'devicon-npm-original-wordmark',
        'yarn': 'devicon-yarn-plain',
        'webpack': 'devicon-webpack-plain',
        'babel': 'devicon-babel-plain',
        'bash': 'devicon-bash-plain',
        'c#': 'devicon-csharp-plain',
        'c++': 'devicon-cplusplus-plain',
        'go': 'devicon-go-plain',
        'java': 'devicon-java-plain',
        'javafx': 'devicon-java-plain', # Using Java icon as proxy for JavaFX
        'socket': 'devicon-apachekafka-original', # Using Kafka as proxy for socket/streaming
        'ollama': 'devicon-google-plain', # Using Google as proxy for AI
        'llama3.1': 'devicon-google-plain', # Using Google as proxy for AI
        'kotlin': 'devicon-kotlin-plain',
        'php': 'devicon-php-plain',
        'ruby': 'devicon-ruby-plain',
        'rust': 'devicon-rust-plain',
        'swift': 'devicon-swift-plain',
        'aws': 'devicon-amazonwebservices-plain-wordmark',
        'azure': 'devicon-azure-plain',
        'google cloud': 'devicon-googlecloud-plain',
        'heroku': 'devicon-heroku-plain',
        'digitalocean': 'devicon-digitalocean-plain',
        'kubernetes': 'devicon-kubernetes-plain',
        'jenkins': 'devicon-jenkins-plain',
        'nextjs': 'devicon-nextjs-plain',
        'next.js': 'devicon-nextjs-plain',
        'tailwindcss': 'devicon-tailwindcss-plain',
        'tailwind': 'devicon-tailwindcss-plain',
        's3': 'devicon-amazonwebservices-plain-wordmark',
        'sass': 'devicon-sass-original',
        'less': 'devicon-less-plain-wordmark',
        'jest': 'devicon-jest-plain',
        'mocha': 'devicon-mocha-plain',
        'selenium': 'devicon-selenium-original',
        'blender': 'devicon-blender-original',
        'photoshop': 'devicon-photoshop-plain',
        'illustrator': 'devicon-illustrator-plain',
        'premiere pro': 'devicon-premierepro-plain',
        'after effects': 'devicon-aftereffects-plain',
        'vscode': 'devicon-vscode-plain',
        'visual studio': 'devicon-visualstudio-plain',
        'pycharm': 'devicon-pycharm-plain',
        'intellij': 'devicon-intellij-plain',
        'webstorm': 'devicon-webstorm-plain',
        'android': 'devicon-android-plain',
        'apple': 'devicon-apple-original',
        'windows': 'devicon-windows8-original',
        'gemini api': 'devicon-google-plain',
        'ai': 'devicon-google-plain',
    }
    
    icon_class = ICON_MAP.get(tech_name_lower, 'devicon-gear-plain') # Default to a gear icon
    
    return format_html('<i class="{0} colored" style="font-size: 1.5rem;" title="{1}"></i>', icon_class, raw_name)


@register.filter
def split_technologies(value):
    """
    Split technologies string by comma/newline and trim surrounding punctuation/spaces.
    """
    if not isinstance(value, str):
        return []

    normalized = value.replace('\r\n', '\n').replace('\n', ',')
    parts = [p.strip() for p in normalized.split(',')]
    cleaned = [re.sub(r'^[\s,]+|[\s,]+$', '', p) for p in parts if p.strip()]
    return cleaned


@register.filter
def bullet_lines(value):
    """
    Convert multi-line text to clean bullet items.
    """
    if not isinstance(value, str):
        return []

    lines = [line.strip() for line in value.splitlines() if line.strip()]
    cleaned = [re.sub(r'^\s*[-*•]\s*', '', line).strip() for line in lines]
    return [line for line in cleaned if line]


@register.filter
def dict_get(mapping, key):
    if isinstance(mapping, dict):
        return mapping.get(key)
    return None
