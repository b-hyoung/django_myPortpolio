from django import template
from django.utils.html import mark_safe, format_html
import markdown

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
    tech_name_lower = technology_name.lower().strip()
    
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
        'kotlin': 'devicon-kotlin-plain',
        'php': 'devicon-php-plain',
        'ruby': 'devicon-ruby-plain',
        'rust': 'devicon-rust-plain',
        'swift': 'devicon-swift-plain',
        'aws': 'devicon-amazonwebservices-original',
        'azure': 'devicon-azure-plain',
        'google cloud': 'devicon-googlecloud-plain',
        'heroku': 'devicon-heroku-plain',
        'digitalocean': 'devicon-digitalocean-plain',
        'kubernetes': 'devicon-kubernetes-plain',
        'jenkins': 'devicon-jenkins-plain',
        'tailwind': 'devicon-tailwindcss-plain',
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
    
    return format_html('<i class="{0} colored" style="font-size: 1.5rem;" title="{1}"></i>', icon_class, technology_name)
