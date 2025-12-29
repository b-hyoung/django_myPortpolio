from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post

class Command(BaseCommand):
    help = 'Creates a new blog post from the given title and content.'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str, help='The title of the blog post.')
        parser.add_argument('content', type=str, help='The content of the blog post.')

    def handle(self, *args, **options):
        title = options['title']
        content = options['content']

        self.stdout.write(self.style.SUCCESS(f'Creating new blog post: "{title}"'))
        
        try:
            # 1. Get Author
            author = User.objects.first()
            if not author:
                self.stdout.write(self.style.ERROR('No users found. Please create a superuser first.'))
                return

            # 2. Create Blog Post
            Post.objects.create(
                author=author,
                title=title,
                content=content.replace('\\n', '\n'), # Replace escaped newlines
            )

            self.stdout.write(self.style.SUCCESS('Successfully created the blog post.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
